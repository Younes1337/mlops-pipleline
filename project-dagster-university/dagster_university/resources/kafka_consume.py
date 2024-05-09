from dagster import resource, Field, String
from confluent_kafka import Consumer
import os

@resource(config_schema={
    "bootstrap_servers": Field(String, description="Kafka broker addresses"),
    "group_id": Field(String, description="Consumer group ID", default_value="my_consumer_group"),
    "topic_name": Field(String, description="Kafka topic name", default_value="test_topic")
})
def kafka_consumer_resource(context):
    bootstrap_servers = os.getenv("KAFKA_BROKER_HOST")
    group_id = context.resource_config["group_id"]
    topic_name = context.resource_config["topic_name"]

    consumer = Consumer({
      'bootstrap.servers': bootstrap_servers,
      'group.id': group_id,
      'topic_name': topic_name,
      'auto.offset.reset': 'earliest'  
  })

    return consumer


# from dagster import resource, Field, String



# @resource(config_schema={
#     "bootstrap_servers": Field(String, description="Kafka broker addresses", default_value="kafka:9092"),
#     "group_id": Field(String, description="Consumer group ID", default_value="my_consumer_group"),
#     "topic_name": Field(String, description="Kafka topic name", default_value="test_topic")
# })
# def kafka_consumer_resource(context):
#     bootstrap_servers = context.resource_config["bootstrap_servers"]
#     group_id = context.resource_config["group_id"]
#     topic_name = context.resource_config["topic_name"]

#     return 