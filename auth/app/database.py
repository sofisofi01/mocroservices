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
        db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@auth_db:5432/authdb")
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def add_to_outbox(self, session, aggregate_id: str, aggregate_type: str, event_type: str, payload: dict):
        outbox_entry = OutboxModel(
            aggregate_id=aggregate_id,
            aggregate_type=aggregate_type,
            event_type=event_type,
            payload=json.dumps(payload),
            created_at=datetime.utcnow()
        )
        session.add(outbox_entry)


db = Database()