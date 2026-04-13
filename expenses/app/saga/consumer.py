import json
import os
import threading
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer
from saga.events import TOPIC, MONTH_CLOSE_REQUESTED, REPORT_CREATED, MONTH_CLOSE_FAILED


def get_producer():
    return KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def validate_expenses(user_id: int, year: int, month: int) -> tuple[bool, str]:
    from database import db
    expenses = db.get_all(user_id)
    month_expenses = [
        e for e in expenses
        if e.date.year == year and e.date.month == month
    ]
    if not month_expenses:
        return False, f"No expenses found for {year}-{month:02d}"
    return True, f"Found {len(month_expenses)} expenses, total: {sum(e.cost * e.quantity for e in month_expenses)}"


def create_report(user_id: int, year: int, month: int) -> dict:
    from database import db
    expenses = db.get_all(user_id)
    month_expenses = [
        e for e in expenses
        if e.date.year == year and e.date.month == month
    ]
    return {
        "user_id": user_id,
        "year": year,
        "month": month,
        "total": sum(e.cost * e.quantity for e in month_expenses),
        "count": len(month_expenses),
        "created_at": datetime.utcnow().isoformat(),
    }


def run():
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    producer = get_producer()

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=bootstrap,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="expenses-saga-group",
        auto_offset_reset="earliest",
    )

    print("Expenses saga consumer started...")

    for message in consumer:
        event = message.value
        event_type = event.get("event_type")

        if event_type != MONTH_CLOSE_REQUESTED:
            continue

        saga_id = event["saga_id"]
        user_id = event["user_id"]
        year = event["year"]
        month = event["month"]

        print(f"[SAGA {saga_id}] Received {event_type} for user {user_id}, {year}-{month:02d}")

        ok, message_text = validate_expenses(user_id, year, month)

        if not ok:
            producer.send(TOPIC, {
                "event_type": MONTH_CLOSE_FAILED,
                "saga_id": saga_id,
                "user_id": user_id,
                "reason": message_text,
            })
            producer.flush()
            print(f"[SAGA {saga_id}] Failed: {message_text}")
            continue

        report = create_report(user_id, year, month)
        producer.send(TOPIC, {
            "event_type": REPORT_CREATED,
            "saga_id": saga_id,
            "user_id": user_id,
            "report": report,
        })
        producer.flush()
        print(f"[SAGA {saga_id}] Report created: {report}")


def start_saga_consumer():
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
