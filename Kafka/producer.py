import logging
import json
import random
import time
from confluent_kafka import Producer

# Function to generate random wine sample data
def generate_random_wine_sample():
    return [
        round(random.uniform(4, 15), 2),
        round(random.uniform(0, 2), 2),
        round(random.uniform(0, 1), 2),
        round(random.uniform(0, 20), 2),
        round(random.uniform(0, 1), 3),
        random.randint(1, 100),
        random.randint(1, 300),
        round(random.uniform(0.9, 1.1), 4),
        round(random.uniform(2.5, 4), 2),
        round(random.uniform(0.1, 2), 2),
        round(random.uniform(8, 15), 1)
    ]

# Function to send wine sample data to Kafka
def send_to_kafka(bootstrap_servers, topic, data):
    try:
        # Create Kafka Producer instance
        producer = Producer({'bootstrap.servers': bootstrap_servers})

        # Produce message to Kafka topic
        producer.produce(topic, json.dumps(data).encode('utf-8'))

        # Flush messages
        producer.flush()

        # Log success message
        logging.info('Wine data sent to Kafka')

        return True, None
    except Exception as e:
        # Log the error message if an exception occurs
        logging.error('Error:')
        return False, str(e)

# Kafka broker address and topic
bootstrap_servers = 'kafka:9092'  # Kafka broker address
topic = 'test_topic'            # Kafka topic to produce messages

# Total duration for sending data (adjustable)
total_duration = 30 * 60  # in seconds (30 minutes)

# Main loop
start_time = time.time()
while time.time() - start_time < total_duration:
    # Generate random wine sample data
    wine_data = generate_random_wine_sample()

    # Send data to Kafka
    connection_status, error_message = send_to_kafka(bootstrap_servers, topic, wine_data)

    # Pause execution for 1 minute
    time.sleep(60)

# Print the result
if connection_status:
    print("Wine data sent to Kafka successfully")
else:
    print("Failed to send wine data to Kafka:", error_message)

