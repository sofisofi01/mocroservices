import os
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
        db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@expenses_db:5432/expensesdb")
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self._load_initial_fixtures()

    def _load_initial_fixtures(self):
        db = self.SessionLocal()
        try:
            from sqlalchemy import func
            if db.query(ExpenseModel).count() == 0:
                expense = ExpenseModel(
                    title="Initial Coffee", 
                    cost=5.5, 
                    quantity=1, 
                    date=date.today(), 
                    owner_id=1
                )
                db.add(expense)
                db.flush()
                
                self._add_to_outbox(db, 
                    aggregate_id=str(expense.id),
                    aggregate_type='expense',
                    event_type='expense_created',
                    payload={
                        'user_id': 1,
                        'expense_id': expense.id,
                        'title': "Initial Coffee",
                        'cost': 5.5
                    }
                )
                db.commit()
                print("Fixtures: Created initial expense and outbox entry.")
        except Exception as e:
            db.rollback()
            print(f"Fixtures error: {e}")
        finally:
            db.close()
    
    def _add_to_outbox(self, session, aggregate_id: str, aggregate_type: str, event_type: str, payload: dict):
        outbox_entry = OutboxModel(
            aggregate_id=aggregate_id,
            aggregate_type=aggregate_type,
            event_type=event_type,
            payload=json.dumps(payload),
            created_at=datetime.utcnow()
        )
        session.add(outbox_entry)

    def create_expense_db(self, title: str, cost: float, quantity: int, expense_date: date, user_id: int) -> ExpenseModel:
        db = self.SessionLocal()
        try:
            expense = ExpenseModel(title=title, cost=cost, quantity=quantity, date=expense_date, owner_id=user_id)
            db.add(expense)
            db.flush()
            
            self._add_to_outbox(db, 
                aggregate_id=str(expense.id),
                aggregate_type='expense',
                event_type='expense_created',
                payload={
                    'user_id': user_id,
                    'expense_id': expense.id,
                    'title': title,
                    'cost': cost
                }
            )
            
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
                
                self._add_to_outbox(db,
                    aggregate_id=str(expense_id),
                    aggregate_type='expense',
                    event_type='expense_updated',
                    payload={
                        'user_id': user_id,
                        'expense_id': expense_id,
                        'updated_fields': list(kwargs.keys())
                    }
                )
                
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
                
                self._add_to_outbox(db,
                    aggregate_id=str(expense_id),
                    aggregate_type='expense',
                    event_type='expense_deleted',
                    payload={
                        'user_id': user_id,
                        'expense_id': expense_id
                    }
                )
                
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()



db = Database()