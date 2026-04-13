import json
import os
import threading
from kafka import KafkaConsumer
from saga.events import TOPIC, REPORT_CREATED, MONTH_CLOSE_FAILED

saga_results: dict = {}


def run():
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=bootstrap,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="auth-saga-group",
        auto_offset_reset="earliest",
    )

    print("Auth saga consumer started...")

    for message in consumer:
        event = message.value
        event_type = event.get("event_type")
        saga_id = event.get("saga_id")

        if event_type == REPORT_CREATED:
            saga_results[saga_id] = {
                "status": "completed",
                "report": event["report"],
            }
            print(f"[SAGA {saga_id}] Month closed successfully. Report: {event['report']}")

        elif event_type == MONTH_CLOSE_FAILED:
            saga_results[saga_id] = {
                "status": "failed",
                "reason": event["reason"],
            }
            print(f"[SAGA {saga_id}] Month close failed: {event['reason']}")


def start_saga_consumer():
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
