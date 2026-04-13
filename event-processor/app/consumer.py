import json
import os
from kafka import KafkaConsumer
from database import get_session, EventLog


def save_to_db(topic: str, event: dict):
    session = get_session()
    try:
        log = EventLog(
            topic=topic,
            event_type=event.get("event_type"),
            user_id=event.get("user_id"),
            payload=json.dumps(event),
        )
        session.add(log)
        session.commit()
    except Exception as e:
        print(f"DB error: {e}")
        session.rollback()
    finally:
        session.close()


def process_event(topic: str, event: dict):
    event_type = event.get("event_type")
    user_id = event.get("user_id")
    print(f"[{topic}] {event_type} | user_id={user_id} | {event}")
    save_to_db(topic, event)


def main():
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    consumer = KafkaConsumer(
        "user-events",
        "expense-events",
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="event-processor-group",
        auto_offset_reset="earliest",
    )

    print("Event processor started. Listening for events...")

    for message in consumer:
        try:
            process_event(message.topic, message.value)
        except Exception as e:
            print(f"Error processing message: {e}")


if __name__ == "__main__":
    main()
