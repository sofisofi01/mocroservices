import os
import json
import threading
from datetime import datetime
from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer
from saga.events import TOPIC, MONTH_CLOSE_REQUESTED, REPORT_CREATED, MONTH_CLOSE_FAILED

def get_avro_consumer(topic, group_id):
    sr_client = SchemaRegistryClient({'url': os.getenv("SCHEMA_REGISTRY_URL", "http://schema-registry:8081")})
    avro_deserializer = AvroDeserializer(sr_client)
    string_deserializer = StringDeserializer('utf_8')

    consumer_conf = {
        'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])
    return consumer, avro_deserializer

def run():
    topic = TOPIC
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")

    conf = {
        'bootstrap.servers': bootstrap,
        'group.id': 'expenses-saga-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    consumer.subscribe([topic])

    print(f"Expenses saga consumer started (JSON) on topic {topic}...")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            try:
                event = json.loads(msg.value().decode('utf-8'))
                if event is None:
                    continue
                
                event_type = event.get("event_type")
                if event_type != MONTH_CLOSE_REQUESTED:
                    continue

                saga_id = event["saga_id"]
                user_id = event["user_id"]
                year = event["year"]
                month = event["month"]

                print(f"[SAGA {saga_id}] Received {event_type} for user {user_id}, {year}-{month:02d}")
            except Exception as e:
                print(f"Error decoding message: {e}")
    finally:
        consumer.close()



def start_saga_consumer():
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
