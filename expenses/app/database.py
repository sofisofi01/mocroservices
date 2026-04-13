import json
from typing import Dict, List, Optional
from datetime import date, datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from database_models import Base, Expense as ExpenseModel, Outbox as OutboxModel

class ExpenseItem:
    def __init__(self, id: int, title: str, cost: float, quantity: int, date: date, user_id:int):
        self.id = id
        self.title = title
        self.cost = cost
        self.quantity = quantity
        self.date = date
        self.user_id = user_id

class Database:
    def __init__(self):
        self.engine = create_engine("sqlite:///expenses.db")
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.expenses: Dict[int, ExpenseItem] = {}
        self.next_id = 1
        self._load_initial_fixtures()
    
    def _add_to_outbox(self, session, topic: str, payload: dict):
        outbox_entry = OutboxModel(
            topic=topic,
            payload=json.dumps(payload),
            created_at=datetime.utcnow(),
            processed=False
        )
        session.add(outbox_entry)

    def create_expense_db(self, title: str, cost: float, quantity: int, expense_date: date, user_id: int) -> ExpenseModel:
        db = self.SessionLocal()
        try:
            expense = ExpenseModel(title=title, cost=cost, quantity=quantity, date=expense_date, owner_id=user_id)
            db.add(expense)
            db.flush() # Чтобы получить ID
            
            self._add_to_outbox(db, 'expense-events', {
                'event_type': 'expense_created',
                'user_id': user_id,
                'expense_id': expense.id,
                'title': title,
                'cost': cost
            })
            
            db.commit()
            db.refresh(expense)
            return expense
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def update_expense_db(self, expense_id: int, user_id: int, **kwargs) -> Optional[ExpenseModel]:
        db = self.SessionLocal()
        try:
            expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id, ExpenseModel.owner_id == user_id).first()
            if expense:
                for key, value in kwargs.items():
                    if hasattr(expense, key) and value is not None:
                        setattr(expense, key, value)
                
                self._add_to_outbox(db, 'expense-events', {
                    'event_type': 'expense_updated',
                    'user_id': user_id,
                    'expense_id': expense_id,
                    'updated_fields': list(kwargs.keys())
                })
                
                db.commit()
                db.refresh(expense)
            return expense
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def delete_expense_db(self, expense_id: int, user_id: int) -> bool:
        db = self.SessionLocal()
        try:
            expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id, ExpenseModel.owner_id == user_id).first()
            if expense:
                db.delete(expense)
                
                self._add_to_outbox(db, 'expense-events', {
                    'event_type': 'expense_deleted',
                    'user_id': user_id,
                    'expense_id': expense_id
                })
                
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

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