from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Date, DateTime, String, Boolean, Text
from datetime import date as date_type, datetime

class Base(DeclarativeBase):
    pass

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    cost: Mapped[float]
    quantity: Mapped[int]
    date: Mapped[date_type] = mapped_column(Date)
    owner_id: Mapped[int] = mapped_column()

class Outbox(Base):
    __tablename__ = "outbox"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic: Mapped[str] = mapped_column(String(255))
    payload: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)