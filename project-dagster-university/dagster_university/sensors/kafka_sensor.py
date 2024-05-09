import json
from dagster import (
    sensor,
    AssetKey,
    SensorEvaluationContext,
    RunRequest,
    asset_sensor
)


# Assuming queue_message and run are defined in assets module
from ..assets.assets import queue_message 
from ..jobs.training_job import train_wine_model



@asset_sensor(asset_key=AssetKey("queue_message"), job=train_wine_model)
def kafka_listener_sensor(context: SensorEvaluationContext):
        
        yield RunRequest(job_name='train_wine_model')
