from dagster import (op, Field, List, String, Int,  # type: ignore
                     DependencyDefinition, 
                     GraphDefinition, 
                     success_hook, 
                     In, Out)

from ..resources.kafka_consume import kafka_consumer_resource
from .ml_training import mlflow_run
import time 
from .data_processing import inferencing_model
from datetime import datetime
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from io import StringIO
from confluent_kafka import KafkaError, Producer
import numpy as np

@op(required_resource_keys={"kafka_consumer"}, 
    out={"result": Out()})

def consume_messages(context, max_messages: int = 100, duration_seconds: int = 60):
    kafka_consumer = context.resources.kafka_consumer
    messages_received = 0
    messages = []
    start_time = time.time()
    
    while messages_received < max_messages and time.time() - start_time <= duration_seconds:
        try:
            # Poll for messages
            msg = kafka_consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition
                    continue
                else:
                    # Handle other errors
                    context.log.error(f"Kafka error: {msg.error()}")
                    break

            # Process the message
            message_content = msg.value().decode('utf-8')  # Decode message value
            context.log.info(f"Received message: {message_content}")
            messages.append(message_content)
            messages_received += 1

        except Exception as e:
            context.log.error(f"Error while consuming message: {e}")
            # Optionally handle the error or break out of the loop
        
    return messages




@op(required_resource_keys={"kafka_consumer"}, 
    ins={"messages": In()},
    out={"result": Out()},
)

def Transform(context, messages):
    kafka_consumer = context.resources.kafka_consumer
    
    # Transform messages into a NumPy array
    data = np.array([message.split('\t') for message in messages])


    # Producer configuration for the transformed data topic
    producer_transformed_data = Producer({
        'bootstrap.servers': 'kafka:9092',
    })

    output_topic = 'transformed_data'  

    # Publish transformed data to the "transformed_data" topic
    producer_transformed_data.produce(output_topic, data)

    # Flush and close the producer
    producer_transformed_data.poll(0)
    producer_transformed_data.flush()
    
    return data


dag_dependencies = {
    "Transform": {
        "messages": DependencyDefinition("consume_messages")
    },
    "inferencing_model": {
        "s3_data":DependencyDefinition("Transform")
    },
    "mlflow_run": {
        "input_data": DependencyDefinition("inferencing_model")
    }, 
}


my_pipeline_graph = GraphDefinition(
    name="my_pipeline",
    description="A pipeline that consumes messages, commits them, and runs an ML job",
    node_defs=[
        consume_messages,
        Transform,
        inferencing_model,
        mlflow_run,
    ],
    dependencies=dag_dependencies
).to_job()