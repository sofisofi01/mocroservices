import time
import json
from database import db
from kafka_producer import KafkaService

def run_relay():
    print("Outbox Relay for Expenses started...")
    while True:
        try:
            pending_messages = db.get_pending_outbox()
            for msg in pending_messages:
                print(f"Processing outbox message {msg.id} for topic {msg.topic}")
                payload = json.loads(msg.payload)
                KafkaService.send_event(msg.topic, payload)
                db.mark_as_processed(msg.id)
            
            if not pending_messages:
                time.sleep(5)
            else:
                time.sleep(1)
        except Exception as e:
            print(f"Error in Outbox Relay: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_relay()
