
## Либка для получения доступа к ресурсам spt

Один раз инициализируете фабрику и потом с помощью методов `get_<recource_name>`(получить креды `get_<recource_name>_credentials`) получаете наобходимый доступ без прописывания всех логинов, явок, паролей

Реализованные ресурсы на текущий момент:

- Доступы к базам
- S3Manager по умолчанию подключается к aws s3 storage. 
- DataVault
- ModelManager
- ModelStorage

## Пример использования
В дс фабрику нужно передать обычную фабрику, что полного использования функционала

Фабрика позволяет получить доступ к `ModelManager` & `PipelineManager`, которые являются singleton'ами

```python
...
spt_factory_resource = MongoFactory(
    mongo_url=os.getenv('MONGO_URL'),
    tlsCAFile=os.getenv('SSLROOT'),
)
spt_ds = DsFactory(spt_factory_resource)
model_manager_1 = spt_ds.get_model_manager()
# Вернет один и тот же объект
model_manager_1 = spt_ds.get_model_manager()
model_manager_2 = spt_ds.get_model_manager()

# Вернет один и тот же объект
pipeline_manager_1 = spt_ds.get_pipeline_manager()
pipeline_manager_2 = spt_ds.get_pipeline_manager()
```

