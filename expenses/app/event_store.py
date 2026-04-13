import json
import os
from typing import List
from kafka import KafkaProducer, KafkaConsumer

TOPIC = "expense-es-events"


class EventStore:
    def __init__(self):
        bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self._bootstrap = bootstrap
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def append(self, event: dict):
        self._producer.send(TOPIC, value=event)
        self._producer.flush()

    def load_all(self) -> List[dict]:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=self._bootstrap,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
        )
        events = [msg.value for msg in consumer]
        consumer.close()
        return events


event_store = EventStore()
