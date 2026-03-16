import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_models import Base


engine_url = os.getenv("DATABASE_URL")

class Database:
    def __init__(self):
        self.engine = create_engine("sqlite:///expenses.db")
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


db = Database()