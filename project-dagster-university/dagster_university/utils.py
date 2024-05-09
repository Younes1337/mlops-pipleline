from confluent_kafka import Consumer, KafkaError

def check_for_new_messages(bootstrap_servers, topic, group_id):

    consumer_conf = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': 'my_consumer_group',
            'auto.offset.reset': 'earliest'
        }
    
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    try:
        while True:
            # Poll for messages with a timeout
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                yield False  # No new message
                continue

            if msg.error():
                # Log Kafka error
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition
                    yield False  # No new message
                else:
                    # Log other Kafka errors
                    yield False  # No new message
                continue

            yield True  # New message received

    except Exception as e:
        # Log the error message if an exception occurs
        print(f'Failed to consume from Kafka: {str(e)}')

    finally:
        consumer.close()
