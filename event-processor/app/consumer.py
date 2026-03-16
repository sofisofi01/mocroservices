import json
import os
from kafka import KafkaConsumer

def process_user_event(event):
    event_type = event.get('event_type')
    login = event.get('login')
    user_id = event.get('user_id')
    
    print(f"Processing event: {event_type} for user {login} (ID: {user_id})")
    
    if event_type == 'user_registered':
        print(f"New user registered: {login}")
    elif event_type == 'user_logged_in':
        print(f"User logged in: {login}")

def process_expense_event(event):
    event_type = event.get('event_type')
    user_id = event.get('user_id')
    expense_id = event.get('expense_id')
    
    print(f"Processing event: {event_type} for expense {expense_id} by user {user_id}")

def main():
    bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    
    consumer = KafkaConsumer(
        'user-events',
        'expense-events',
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='event-processor-group',
        auto_offset_reset='earliest'
    )
    
    print("Event processor started. Listening for events...")
    
    for message in consumer:
        try:
            event = message.value
            topic = message.topic
            
            if topic == 'user-events':
                process_user_event(event)
            elif topic == 'expense-events':
                process_expense_event(event)
                
        except Exception as e:
            print(f"Error processing message: {e}")

if __name__ == "__main__":
    main()
