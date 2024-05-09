from dagster import ( # type: ignore
    AssetSelection,
    Definitions,
    load_assets_from_modules,
    RepositoryDefinition,
    ScheduleDefinition, 
    define_asset_job
    
)
from .resources.kafka_consume import kafka_consumer_resource
from . import assets 
from .sensors.kafka_sensor import kafka_listener_sensor  # Import your sensor function from the sensors module
from .jobs.training_job import train_wine_model
from .assets.assets import queue_message
from .ops.Kafka_ops import my_pipeline_graph


# Load assets from modules
all_assets = load_assets_from_modules([assets]) 

job_scheduler = ScheduleDefinition(
    job=my_pipeline_graph,
    cron_schedule="*/3 * * * * "
)

defs = Definitions(
    assets=all_assets,
    sensors=[kafka_listener_sensor],  # Pass the sensor function within a list
    jobs=[train_wine_model, my_pipeline_graph],
    resources={"kafka_consumer": kafka_consumer_resource}, 
    schedules=[job_scheduler]
)

