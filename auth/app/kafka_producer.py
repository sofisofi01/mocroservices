import json
import os
from confluent_kafka import Producer

class KafkaService:
    _producer = None

    @classmethod
    def get_producer(cls):
        if cls._producer is None:
            bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
            conf = {
                'bootstrap.servers': bootstrap_servers,
                'client.id': 'auth-service'
            }
            cls._producer = Producer(conf)
        return cls._producer

    @classmethod
    def send_event(cls, topic: str, event_data: dict):
        try:
            producer = cls.get_producer()
            producer.produce(topic, value=json.dumps(event_data).encode('utf-8'))
            producer.flush()
        except Exception as e:
            print(f"Error sending event: {e}")
