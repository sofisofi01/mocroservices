import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime


class Base(DeclarativeBase):
    pass


class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True)
    topic = Column(String(100))
    event_type = Column(String(100))
    user_id = Column(Integer, nullable=True)
    payload = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_session():
    url = os.getenv("DATABASE_URL")
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
