import logging
from confluent_kafka import Consumer, KafkaError

# Function to consume messages from Kafka
def consume_from_kafka(bootstrap_servers, group_id, topic):
    try:
        # Create Kafka Consumer instance
        consumer_conf = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        }
        consumer = Consumer(consumer_conf)

        # Subscribe to the Kafka topic
        consumer.subscribe([topic])

        # Consume messages from Kafka
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition, ignore
                    continue
                else:
                    # Log any other error
                    logging.error(f'Kafka consumer error: {msg.error()}')
                    break

            # Print consumed message
            print(f'Consumed message: {msg.value().decode("utf-8")}')

    except KeyboardInterrupt:
        # Handle keyboard interrupt gracefully
        logging.info('Consumer interrupted, closing...')
    finally:
        # Close Kafka Consumer
        consumer.close()

# Call the consume_from_kafka function
if __name__ == "__main__":
    bootstrap_servers = 'kafka:9092'  # Kafka broker address
    group_id = 'test_consumer_group'   # Kafka consumer group ID
    topic = 'test_topic'               # Kafka topic to consume messages
    consume_from_kafka(bootstrap_servers, group_id, topic)

