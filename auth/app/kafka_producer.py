import json
import os
from kafka import KafkaProducer
from kafka.errors import KafkaError

class KafkaService:
    _producer = None

    @classmethod
    def get_producer(cls):
        if cls._producer is None:
            bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
            cls._producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        return cls._producer

    @classmethod
    def send_event(cls, topic: str, event_data: dict):
        try:
            producer = cls.get_producer()
            future = producer.send(topic, event_data)
            future.get(timeout=10)
        except KafkaError as e:
            print(f"Kafka error: {e}")
        except Exception as e:
            print(f"Error sending event: {e}")
