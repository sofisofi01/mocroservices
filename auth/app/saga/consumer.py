import json
import os
import threading
from confluent_kafka import Consumer
from saga.events import TOPIC, REPORT_CREATED, MONTH_CLOSE_FAILED

saga_results: dict = {}

def run():
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")

    conf = {
        'bootstrap.servers': bootstrap,
        'group.id': 'auth-saga-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    consumer.subscribe([TOPIC])

    print("Auth saga consumer started...")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            try:
                # Простая десериализация JSON (без Avro для этого топика пока что)
                event = json.loads(msg.value().decode('utf-8'))
                event_type = event.get("event_type")
                saga_id = event.get("saga_id")

                if event_type == REPORT_CREATED:
                    saga_results[saga_id] = {
                        "status": "completed",
                        "report": event["report"],
                    }
                    print(f"[SAGA {saga_id}] Month closed successfully.")

                elif event_type == MONTH_CLOSE_FAILED:
                    saga_results[saga_id] = {
                        "status": "failed",
                        "reason": event["reason"],
                    }
                    print(f"[SAGA {saga_id}] Month close failed.")
            except Exception as e:
                print(f"Error processing message: {e}")
    finally:
        consumer.close()


def start_saga_consumer():
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
