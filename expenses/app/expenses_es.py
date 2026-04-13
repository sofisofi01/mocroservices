from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import date
from typing import Optional
import uuid

from models import Expense, ExpenseUpdate
from crypt import CryptService
from event_store import event_store
from projections import replay, replay_one

router = APIRouter(prefix="/es", tags=["expenses-es"])
security = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(security)) -> int:
    try:
        user_id = CryptService.decode_token(token)
        if not user_id:
            raise HTTPException(status_code=401, detail="User not found")
        return user_id
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")



@router.post("/expenses", status_code=201)
def create_expense(expense: Expense, user_id: int = Depends(get_current_user)):
    expense_id = str(uuid.uuid4())
    event_store.append({
        "event_type": "ExpenseCreated",
        "expense_id": expense_id,
        "user_id": user_id,
        "title": expense.title,
        "cost": expense.cost,
        "quantity": expense.quantity,
        "date": str(expense.date or date.today()),
    })
    return {"expense_id": expense_id}


@router.patch("/expenses/{expense_id}")
def update_expense(expense_id: str, data: ExpenseUpdate, expected_version: int, user_id: int = Depends(get_current_user)):
    events = event_store.load_all()
    current = replay_one(events, expense_id)
    if not current:
        raise HTTPException(status_code=404, detail="Expense not found")

    if current["version"] != expected_version:
        raise HTTPException(
            status_code=409,
            detail=f"Version conflict: expected {expected_version}, current {current['version']}"
        )

    event_store.append({
        "event_type": "ExpenseUpdated",
        "expense_id": expense_id,
        "user_id": user_id,
        "title": data.title,
        "cost": data.cost,
        "quantity": data.quantity,
        "date": str(data.date) if data.date else None,
    })
    return {"expense_id": expense_id, "version": current["version"] + 1}


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str, user_id: int = Depends(get_current_user)):
    events = event_store.load_all()
    if not replay_one(events, expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")

    event_store.append({
        "event_type": "ExpenseDeleted",
        "expense_id": expense_id,
        "user_id": user_id,
    })
    return {"expense_id": expense_id}

@router.get("/expenses")
def get_expenses(user_id: int = Depends(get_current_user)):
    events = event_store.load_all()
    all_expenses = replay(events)
    return [e for e in all_expenses.values() if e["user_id"] == user_id]


@router.get("/expenses/{expense_id}")
def get_expense(expense_id: str, user_id: int = Depends(get_current_user)):
    events = event_store.load_all()
    expense = replay_one(events, expense_id)
    if not expense or expense["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.get("/expenses/{expense_id}/history")
def get_history(expense_id: str, user_id: int = Depends(get_current_user)):
    events = event_store.load_all()
    return [e for e in events if str(e.get("expense_id")) == expense_id]
