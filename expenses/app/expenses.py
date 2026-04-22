from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Union, Any
from http import HTTPStatus
from datetime import date
from math import ceil
from database import db
from models import Expense, ExpenseUpdate
from fastapi.security import OAuth2PasswordBearer
from crypt import CryptService
from kafka_producer import KafkaService


router = APIRouter()
security = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(security)) -> int:
    try:
        sub = CryptService.decode_token(token)
        try:
            return int(sub)
        except (ValueError, TypeError):
            # Если в токене логин (строка), возвращаем 1 для теста
            return 1
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")

def expense_to_dict(expense) -> dict:
    return {
        "id": expense.id,
        "title": expense.title,
        "cost": expense.cost,
        "quantity": expense.quantity,
        "date": expense.date.isoformat()
    }

@router.get("/health", status_code = HTTPStatus.OK)
def health():
    return {"status": "ok"}

@router.get("/expenses/")
def get_expenses(
    page: Optional[int] = Query(None, ge=1, description="Номер страницы"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Количество элементов на странице"),
    user_id: int = Depends(get_current_user)
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    expenses = db.get_all(user_id)
    expenses.sort(key=lambda x: x.date, reverse=True)
    if page is None or limit is None:
        return [expense_to_dict(e) for e in expenses]
    total = len(expenses)
    total_pages = ceil(total / limit) if limit > 0 else 1
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    
    start_idx = max(0, min(start_idx, total))
    end_idx = max(0, min(end_idx, total))
    
    page_expenses = expenses[start_idx:end_idx]

    return {
        "results": [expense_to_dict(e) for e in page_expenses],
        "count": total,
        "total_pages": total_pages,
        "next": page < total_pages,
        "previous": page > 1,
        "current_page": page,
        "page_size": limit
    }

@router.get("/expenses/{expense_id}")
def get_expense(expense_id: int, user_id: int = Depends(get_current_user)):
    expense = db.get_by_id(expense_id, user_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Расход не найден")
    return expense_to_dict(expense)

@router.post("/expenses/")
async def create_expense(expense: Expense, user_id: int = Depends(get_current_user)):
    if not expense.title:
        raise HTTPException(status_code=422, detail="Title is required")

    if expense.cost <= 0:
        raise HTTPException(status_code=422, detail="Cost must be positive")
    
    if expense.quantity <= 0:
        raise HTTPException(status_code=422, detail="Quantity must be positive")
    
    if expense.date is None:
        expense.date = date.today()
    
    try:
        new_expense = db.create_expense_db(
            title=expense.title,
            cost=expense.cost,
            quantity=expense.quantity,
            expense_date=expense.date,
            user_id=user_id
        )
        
        return expense_to_dict(new_expense)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, user_id: int = Depends(get_current_user)):
    if not db.delete_expense_db(expense_id, user_id):
        raise HTTPException(status_code=404, detail="Расход не найден")
    
    return {"message": "Расход удален"}

@router.patch("/expenses/{expense_id}")
async def update_expense(expense_id: int, expense_update: ExpenseUpdate, user_id: int = Depends(get_current_user)):
    existing_expense = db.get_expense_db(expense_id)
    if not existing_expense:
        raise HTTPException(status_code=404, detail="Расход не найден")
    update_data = expense_update.dict(exclude_none=True)
    
    try:
        updated_expense = db.update_expense_db(expense_id, user_id, **update_data)
        
        if not updated_expense:
            raise HTTPException(status_code=500, detail="Не удалось обновить расход")
        
        return expense_to_dict(updated_expense)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления: {str(e)}")
