##################################################### MLFLOW TESTING ########################################
from dagster import asset, MaterializeResult
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import mlflow
import logging
import boto3
from botocore.exceptions import ClientError
from confluent_kafka import (
    Producer, 
    Consumer, 
    KafkaError,
)
from datetime import datetime, timedelta

import json
import os 

@asset
def establish_kafka_connection(context) -> MaterializeResult:
    bootstrap_servers = "kafka:9092"  # Specify Kafka bootstrap servers here
    try:
        # Create Kafka Producer instance
        producer = Producer({'bootstrap.servers': bootstrap_servers})

        # Log success message
        context.log.info('Connection to Kafka established successfully')
        return MaterializeResult(
            metadata = {
                "Message": "Connection to kafka established succ!", 
            }
        )
    except Exception as e:
        # Log the error message if an exception occurs
        context.log.error(f'Failed to establish connection to Kafka: {str(e)}')
        raise MaterializeResult(
            metadata= {
                "Message": f"An error : {e} ! Shutdown the docker-compose and build again !",
            }
        )


from datetime import datetime, timedelta

@asset(deps=[establish_kafka_connection])
def queue_message(context) -> MaterializeResult:
    bootstrap_servers = "kafka:9092"
    topic = "test_topic"
    
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=1)  # Set end time to one minute from start

    try:
        # Create Kafka Consumer instance
        consumer_conf = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': 'my_consumer_group',
            'auto.offset.reset': 'earliest'
        }
        consumer = Consumer(consumer_conf)

        # Subscribe to Kafka topic
        consumer.subscribe([topic])

        # List to store consumed messages
        consumed_data = []

        def consume_from_kafka():
            try:
                while True:  # Consume data until one minute duration
                    # Poll for messages with a timeout
                    msg = consumer.poll(timeout=1.0)
                    if msg is None:
                        continue

                    if msg.error():
                        # Log Kafka error
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            # End of partition
                            context.log.info(f'Reached end of partition {msg.topic()} [{msg.partition()}]')
                        else:
                            # Log other Kafka errors
                            context.log.error(f'Kafka error: {msg.error()}')
                        continue

                    # Store received message value in the list
                    consumed_data.append(msg.value().decode("utf-8"))
                    context.log.info(f"Consumed message: {msg.value().decode('utf-8')}")
            except Exception as e:
                # Log the error message if an exception occurs
                context.log.error(f'Failed to consume from Kafka: {str(e)}')
                raise e

        # Consume messages from Kafka
        consume_from_kafka()

        # Materialize consumed data
        context.log.info(f"Consumed {len(consumed_data)} messages")
        return MaterializeResult(
            metadata={
                "status": "success",
                "data": consumed_data,
            },
        )

    except Exception as e:
        # Log the error message in case of exception
        context.log.error(f'Failed to establish connection to Kafka: {str(e)}')
        # Raise a Materialization with error message and status
        raise MaterializeResult(
            metadata={
                "status": "failure",
                "message": f"Failed to establish connection to Kafka: {str(e)}"
            },
        )
     