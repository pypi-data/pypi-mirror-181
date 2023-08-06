from abc import ABC, abstractmethod
from importlib import import_module

from spt_datascience.datascience.models.base_model import BaseModel, ModelConfig
from spt_datascience.datascience.singleton import Singleton

MODELS_BUCKET = 'theme-models'


class ModelStorage():

    @abstractmethod
    def upload_model_bins(self, model_config):
        pass

    @abstractmethod
    def load_model_bins(self, model_config):
        pass


class S3ModelStorage(ModelStorage, metaclass=Singleton):

    def __init__(self, spt_resource_factory):
        self.s3_client = spt_resource_factory.get_s3_manager()
        self.mongo_client = spt_resource_factory.get_mongo()

    def upload_model_bins(self, model_config):
        for bin_name, bin_obj in model_config.bins.items():
            model_path = model_config.id + '/' + bin_name
            self.s3_client.upload_bin(bucket_name=MODELS_BUCKET, id=model_path, bin_str=bin_obj)
            model_config.bins[bin_name] = model_path
        return model_config

    def load_model_bins(self, model_config):
        model_bins = model_config.bins
        model_bucket = MODELS_BUCKET
        for bin_name, bin_path in model_bins.items():
            model_bins[bin_name] = self.s3_client.download_bin(bucket_name=model_bucket, id=bin_path)
        model_config.bins = model_bins
        return model_config

    def delete_model(self, model_id):
        self.mongo_client.spt.models.delete_one({'id': model_id})
        self.s3_client.delete_folder(MODELS_BUCKET, model_id)


class MLFlowSklearnModelStorage(ModelStorage, metaclass=Singleton):

    def __init__(self, spt_resource_factory, ds_factory):
        self.spt_resource_factory = spt_resource_factory
        self.ds_factory = ds_factory
        self.mlflow = ds_factory.get_mlflow()

    def upload_model_bins(self, model_config):
        raise NotImplemented("Save mlflow model using mlflow API")

    def load_model_bins(self, model_config):
        model_bins = model_config.bins
        for bin_name, bin_value in model_bins.items():
            model_uri = f"models:/{bin_value['name']}/{bin_value['version']}"
            model_bins[bin_name] = self.mlflow.sklearn.load_model(model_uri)
        return model_config

