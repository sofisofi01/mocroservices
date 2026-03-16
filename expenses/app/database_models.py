from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Date
from datetime import date as date_type

class Base(DeclarativeBase):
    pass

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    cost: Mapped[float]
    quantity: Mapped[int]
    date: Mapped[date_type] = mapped_column(Date)
    owner_id: Mapped[int] = mapped_column