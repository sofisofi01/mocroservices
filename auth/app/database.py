import os
import json
from datetime import datetime
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_models import Base, Outbox as OutboxModel


engine_url = os.getenv("DATABASE_URL")

class Database:
    def __init__(self):
        self.engine = create_engine("sqlite:///expenses.db")
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def add_to_outbox(self, session, topic: str, payload: dict):
        outbox_entry = OutboxModel(
            topic=topic,
            payload=json.dumps(payload),
            created_at=datetime.utcnow(),
            processed=False
        )
        session.add(outbox_entry)

    def get_pending_outbox(self) -> List[OutboxModel]:
        db = self.SessionLocal()
        messages = db.query(OutboxModel).filter(OutboxModel.processed == False).all()
        db.close()
        return messages

    def mark_as_processed(self, message_id: int):
        db = self.SessionLocal()
        message = db.query(OutboxModel).filter(OutboxModel.id == message_id).first()
        if message:
            message.processed = True
            db.commit()
        db.close()


db = Database()