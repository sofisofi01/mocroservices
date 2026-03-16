from pydantic import BaseModel, Field
from datetime import date as DateClass 
from typing import Optional, Annotated

TitleType = Annotated[str, Field(min_length=1, max_length=100)]
CostType = Annotated[float, Field(gt=0)]
QuantityType = Annotated[int, Field(gt=0)]
DateType = Optional[DateClass]
LoginType = Annotated[str, Field(min_length=3, max_length=50)]
PasswordType = Annotated[str, Field(min_length=6, max_length=36)]
TokenType = Annotated[str, Field()]

class Expense(BaseModel):
    title: TitleType
    cost: CostType
    quantity: QuantityType
    date: DateType = None

class ExpenseCreate(Expense):
    pass

class ExpenseUpdate(BaseModel):
    title: Optional[TitleType] = None
    cost: Optional[CostType] = None
    quantity: Optional[QuantityType] = None
    date: DateType = None

class ExpenseResponse(Expense):
    id: int
    