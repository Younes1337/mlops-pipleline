import pandas as pd
import boto3 
import numpy as np
from dagster import op, In, Out
from datasets import Dataset
from datasets import load_dataset
from datasets import Dataset
from setfit import get_templated_dataset
from huggingface_hub import login
from setfit import TrainingArguments, Trainer, SetFitModel
from setfit import sample_dataset
from confluent_kafka import Consumer, KafkaError, KafkaException

@op(ins={"s3_data": In()}, out={"result": Out()})
def inferencing_model(context, s3_data):
    try:
        # Configure Kafka consumer
        kafka_consumer_config = {
            'bootstrap.servers': 'kafka:9092',
            'group.id': 'my_consumer_group',
            'auto.offset.reset': 'earliest'
        }
        kafka_consumer = Consumer(kafka_consumer_config)

        # Subscribe to the "transformed_data" topic
        kafka_consumer.subscribe(['transformed_data'])

        # Poll for messages
        while True:
            msg = kafka_consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition
                    context.log.warning('%% %s [%d] reached end at offset %d\n' %
                                        (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Process the message
                transformed_data = msg  # Assuming data is UTF-8 encoded
                context.log.info(f"Received data from Kafka: {transformed_data}")

                """
                # Perform inference with the received data
                try:
                    login('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')
                    model = SetFitModel.from_pretrained("EffyisDATALAB/setfit_trx_classification_OrdalieTech_Solon-embeddings-large-0.1_particular_91.67_CRDT")
                    test_dataset = transformed_data

                    results = model.predict(test_dataset)

                    context.log.info(f"Inference results: {results}")
                    
                    # Return the results
                    return results

                except Exception as e:
                    context.log.error(f"Inference failed: {e}")
                """    

    finally:
        # Close Kafka consumer
        kafka_consumer.close()
