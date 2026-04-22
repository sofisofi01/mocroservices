import json
import os
import threading
from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
from saga.events import TOPIC, REPORT_CREATED, MONTH_CLOSE_FAILED

saga_results: dict = {}

def run():
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
    sr_url = os.getenv("SCHEMA_REGISTRY_URL", "http://schema-registry:8081")

    sr_client = SchemaRegistryClient({'url': sr_url})
    avro_deserializer = AvroDeserializer(sr_client)

    conf = {
        'bootstrap.servers': bootstrap,
        'group.id': 'auth-saga-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    consumer.subscribe([TOPIC])

    print("Auth saga consumer started (Avro)...")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            try:
                ctx = SerializationContext(TOPIC, MessageField.VALUE)
                event = avro_deserializer(msg.value(), ctx)
                
                if event is None or not isinstance(event, dict):
                    continue

                event_type = event.get("event_type")
                saga_id = event.get("saga_id")

                if event_type == REPORT_CREATED:
                    saga_results[saga_id] = {
                        "status": "completed",
                        "report": event["report"],
                    }
                    print(f"[SAGA {saga_id}] Month closed successfully.", flush=True)

                elif event_type == MONTH_CLOSE_FAILED:
                    saga_results[saga_id] = {
                        "status": "failed",
                        "reason": event["reason"],
                    }
                    print(f"[SAGA {saga_id}] Month close failed.", flush=True)
            except Exception as e:
                print(f"Error processing message: {e}", flush=True)
    finally:
        consumer.close()


def start_saga_consumer():
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
