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

def validate_expenses(user_id: int, year: int, month: int) -> tuple[bool, str]:
    from database import db
    session = db.SessionLocal()
    try:
        from database_models import Expense as ExpenseModel
        expenses = session.query(ExpenseModel).filter(ExpenseModel.owner_id == user_id).all()
        month_expenses = [
            e for e in expenses
            if e.date.year == year and e.date.month == month
        ]
        if not month_expenses:
            return False, f"No expenses found for {year}-{month:02d}"
        return True, f"Found {len(month_expenses)} expenses"
    finally:
        session.close()

def create_report(user_id: int, year: int, month: int) -> dict:
    from database import db
    session = db.SessionLocal()
    try:
        from database_models import Expense as ExpenseModel
        expenses = session.query(ExpenseModel).filter(ExpenseModel.owner_id == user_id).all()
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
    finally:
        session.close()

def run():
    try:
        print("DEBUG: Starting saga consumer thread...", flush=True)
        topic = TOPIC
        bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")

        conf = {
            'bootstrap.servers': bootstrap,
            'group.id': 'expenses-saga-group',
            'auto.offset.reset': 'earliest'
        }

        consumer = Consumer(conf)
        consumer.subscribe([topic])

        print(f"Expenses saga consumer started (JSON) on topic {topic}...", flush=True)

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}", flush=True)
                continue

            try:
                raw_value = msg.value().decode('utf-8')
                event = json.loads(raw_value)
                
                # Если Debezium прислал payload как строку внутри JSON, декодируем еще раз
                if isinstance(event, str):
                    event = json.loads(event)
                
                if event is None or not isinstance(event, dict):
                    continue
                
                event_type = event.get("event_type")
                if event_type != MONTH_CLOSE_REQUESTED:
                    continue

                saga_id = event["saga_id"]
                user_id = event["user_id"]
                year = event["year"]
                month = event["month"]

                print(f"[SAGA {saga_id}] Received {event_type} for user {user_id}, {year}-{month:02d}", flush=True)

                from database import db
                ok, message_text = validate_expenses(user_id, year, month)

                session = db.SessionLocal()
                try:
                    if not ok:
                        db._add_to_outbox(session,
                            aggregate_id=saga_id,
                            aggregate_type='saga',
                            event_type=MONTH_CLOSE_FAILED,
                            payload={
                                "event_type": MONTH_CLOSE_FAILED,
                                "saga_id": saga_id,
                                "user_id": user_id,
                                "reason": message_text,
                            }
                        )
                        print(f"[SAGA {saga_id}] Failed: {message_text}", flush=True)
                    else:
                        report = create_report(user_id, year, month)
                        db._add_to_outbox(session,
                            aggregate_id=saga_id,
                            aggregate_type='saga',
                            event_type=REPORT_CREATED,
                            payload={
                                "event_type": REPORT_CREATED,
                                "saga_id": saga_id,
                                "user_id": user_id,
                                "report": report,
                            }
                        )
                        print(f"[SAGA {saga_id}] Report created", flush=True)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print(f"[SAGA {saga_id}] Error saving response to outbox: {e}", flush=True)
                finally:
                    session.close()
            except Exception as e:
                print(f"Error decoding message: {e}", flush=True)
    except Exception as e:
        print(f"CRITICAL: Saga consumer thread failed to start: {e}", flush=True)
    finally:
        try:
            consumer.close()
        except:
            pass



def start_saga_consumer():
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
