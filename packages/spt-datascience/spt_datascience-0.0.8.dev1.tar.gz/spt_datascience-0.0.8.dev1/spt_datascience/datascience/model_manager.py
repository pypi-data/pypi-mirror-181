from abc import abstractmethod
from importlib import import_module

import ulid

from spt_datascience.datascience.model_util import ModelUtil, MongoModelUtil
from spt_datascience.datascience.models.base_model import BaseModel, ModelConfig
from functools import lru_cache
from spt_datascience.datascience.singleton import Singleton
from spt_datascience.datascience.models_storage import S3ModelStorage
from spt_datascience.datascience.models_storage import MLFlowSklearnModelStorage


class ModelManager(metaclass=Singleton):

    @abstractmethod
    def get_model(self, model_id) -> BaseModel:
        """
        Return model object by id
        :param model_id: id of the model
        :return:
        """
        pass

    @abstractmethod
    def save_model(self, model, storage_type) -> str:
        """
        Save model and return model id
        :param model: model inherit from BaseModel
        :return: model id
        """
        pass

    @abstractmethod
    def get_model_config(self, model_id, storage_type) -> ModelConfig:
        """
        Return model object by id
        :param model_id: id of the model
        :return:
        """
        pass

    @abstractmethod
    def save_model_config(self, model_config, storage_type):
        """
        Save model config
        :param model: model inherit from BaseModel
        """
        pass


class SPTModelManager(ModelManager):

    def __init__(self, spt_resource_factory, spt_ds_factory):
        self.ds_factory = spt_ds_factory
        self.model_util = MongoModelUtil(spt_resource_factory)
        self.model_storages = {
            's3': S3ModelStorage(spt_resource_factory),
            'mlflow/sklearn': MLFlowSklearnModelStorage(spt_resource_factory, spt_ds_factory)
        }
        self.spt_resource_factory = spt_resource_factory

    @lru_cache(maxsize=1024)
    def get_model(self, model_id) -> BaseModel:
        model_config = self.get_model_config(model_id)
        model_package = model_config.model_package
        model_class = model_config.model_class
        return self._load_model_object(model_package, model_class, model_config)

    def save_model(self, model: BaseModel, storage_type: str = 's3') -> str:
        model_name = model.model_name()
        model_version = self.increment_model_version(self.model_util.get_model_version(model_name))
        model_id = self.produce_model_id(model_name, model_version)
        model_config = model.save_model(model_id, model_version)
        self.save_model_config(model_config, storage_type)
        return model_id

    def produce_model_id(self, model_name, model_version):
        return f"{model_name}{model_version}#{ulid.new().str}"

    def increment_model_version(self, version):
        return version + 1

    def get_model_config(self, model_id, storage_type: str = 's3'):
        with self.spt_resource_factory.get_mongo() as mongo_client:
            model_config_dict = mongo_client.spt.models.find_one({'id': model_id})
        storage_type = model_config_dict.get('storage_type', storage_type)
        model_config = ModelConfig.from_dict(model_config_dict)
        return self.model_storages[storage_type].load_model_bins(model_config)

    def save_model_config(self, model_config, storage_type: str = 's3'):
        storage_type = model_config.storage_type if model_config.storage_type else storage_type
        model_config = self.model_storages[storage_type].upload_model_bins(model_config)
        self.model_util.save_model_config(model_config)

    def delete_model(self, model_id, storage_type: str = 's3'):
        self.model_storages[storage_type].delete_model(model_id)

    def _load_model_object(self, model_package, model_class, model_config):
        module = import_module(model_package)
        return getattr(
            module, model_class
        ).load_model(model_config)
