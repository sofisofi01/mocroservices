from typing import Dict, List, Optional
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_models import Base, Expense as ExpenseModel

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
    
    def _load_initial_fixtures(self):
        initial_fixtures = [
    {"id": 1, "title": "Ноутбук", "cost": 75000.00, "quantity": 1, "date": date(2024, 1, 15)},
    {"id": 2, "title": "Смартфон", "cost": 45000.00, "quantity": 2, "date": date(2024, 1, 16)},
    {"id": 3, "title": "Наушники", "cost": 5000.00, "quantity": 3, "date": date(2024, 1, 17)},
    {"id": 4, "title": "Клавиатура", "cost": 2500.00, "quantity": 1, "date": date(2024, 1, 18)},
    {"id": 5, "title": "Монитор", "cost": 30000.00, "quantity": 1, "date": date(2024, 1, 19)},
    {"id": 6, "title": "Компьютерная мышь", "cost": 1500.00, "quantity": 2, "date": date(2024, 1, 20)},
    {"id": 7, "title": "Принтер", "cost": 12000.00, "quantity": 1, "date": date(2024, 1, 21)},
    {"id": 8, "title": "Сканер", "cost": 8000.00, "quantity": 1, "date": date(2024, 1, 22)},
    {"id": 9, "title": "Колонки", "cost": 3500.00, "quantity": 1, "date": date(2024, 1, 23)},
    {"id": 10, "title": "Веб-камера", "cost": 3000.00, "quantity": 2, "date": date(2024, 1, 24)},
    {"id": 11, "title": "Холодильник", "cost": 40000.00, "quantity": 1, "date": date(2024, 1, 25)},
    {"id": 12, "title": "Стиральная машина", "cost": 35000.00, "quantity": 1, "date": date(2024, 1, 26)},
    {"id": 13, "title": "Посудомоечная машина", "cost": 28000.00, "quantity": 1, "date": date(2024, 1, 27)},
    {"id": 14, "title": "Микроволновая печь", "cost": 8000.00, "quantity": 1, "date": date(2024, 1, 28)},
    {"id": 15, "title": "Пылесос", "cost": 12000.00, "quantity": 1, "date": date(2024, 1, 29)},
    {"id": 16, "title": "Чайник электрический", "cost": 2500.00, "quantity": 1, "date": date(2024, 1, 30)},
    {"id": 17, "title": "Кофеварка", "cost": 15000.00, "quantity": 1, "date": date(2024, 1, 31)},
    {"id": 18, "title": "Диван", "cost": 45000.00, "quantity": 1, "date": date(2024, 2, 1)},
    {"id": 19, "title": "Кровать", "cost": 30000.00, "quantity": 1, "date": date(2024, 2, 2)},
    {"id": 20, "title": "Стол компьютерный", "cost": 12000.00, "quantity": 1, "date": date(2024, 2, 3)},
    {"id": 21, "title": "Офисное кресло", "cost": 15000.00, "quantity": 1, "date": date(2024, 2, 4)},
    {"id": 22, "title": "Книжная полка", "cost": 8000.00, "quantity": 2, "date": date(2024, 2, 5)},
    {"id": 23, "title": "Тумба под телевизор", "cost": 9500.00, "quantity": 1, "date": date(2024, 2, 6)},
    {"id": 24, "title": "Бензин АИ-95", "cost": 2500.00, "quantity": 1, "date": date(2024, 2, 7)},
    {"id": 25, "title": "Масло моторное", "cost": 4500.00, "quantity": 1, "date": date(2024, 2, 8)},
    {"id": 26, "title": "Шиномонтаж", "cost": 3000.00, "quantity": 1, "date": date(2024, 2, 9)},
    {"id": 27, "title": "Техническое обслуживание", "cost": 15000.00, "quantity": 1, "date": date(2024, 2, 10)},
    {"id": 28, "title": "Страховка ОСАГО", "cost": 12000.00, "quantity": 1, "date": date(2024, 2, 11)},
    {"id": 29, "title": "Парковка", "cost": 500.00, "quantity": 30, "date": date(2024, 2, 12)},  # месячный абонемент
    {"id": 30, "title": "Продукты на неделю", "cost": 5000.00, "quantity": 1, "date": date(2024, 2, 13)},
    {"id": 31, "title": "Кофе в зернах", "cost": 1200.00, "quantity": 2, "date": date(2024, 2, 14)},
    {"id": 32, "title": "Молоко", "cost": 90.00, "quantity": 10, "date": date(2024, 2, 15)},
    {"id": 33, "title": "Хлеб", "cost": 50.00, "quantity": 15, "date": date(2024, 2, 16)},
    {"id": 34, "title": "Яйца", "cost": 120.00, "quantity": 5, "date": date(2024, 2, 17)},
    {"id": 35, "title": "Мясо куриное", "cost": 350.00, "quantity": 3, "date": date(2024, 2, 18)},
    {"id": 36, "title": "Фрукты", "cost": 800.00, "quantity": 1, "date": date(2024, 2, 19)},
    {"id": 37, "title": "Овощи", "cost": 600.00, "quantity": 1, "date": date(2024, 2, 20)},
    {"id": 38, "title": "Билеты в кино", "cost": 800.00, "quantity": 2, "date": date(2024, 2, 21)},
    {"id": 39, "title": "Ужин в ресторане", "cost": 3500.00, "quantity": 1, "date": date(2024, 2, 22)},
    {"id": 40, "title": "Абонемент в спортзал", "cost": 3000.00, "quantity": 1, "date": date(2024, 2, 23)},
    {"id": 41, "title": "Концерт", "cost": 2500.00, "quantity": 2, "date": date(2024, 2, 24)},
    {"id": 42, "title": "Книги", "cost": 1500.00, "quantity": 5, "date": date(2024, 2, 25)},
    {"id": 43, "title": "Подписка на стриминг", "cost": 399.00, "quantity": 1, "date": date(2024, 2, 26)},
    {"id": 44, "title": "Коммунальные услуги", "cost": 7500.00, "quantity": 1, "date": date(2024, 2, 27)},
    {"id": 45, "title": "Интернет", "cost": 800.00, "quantity": 1, "date": date(2024, 2, 28)},
    {"id": 46, "title": "Мобильная связь", "cost": 500.00, "quantity": 1, "date": date(2024, 2, 29)},
    {"id": 47, "title": "Электричество", "cost": 2500.00, "quantity": 1, "date": date(2024, 3, 1)},
    {"id": 48, "title": "Вода", "cost": 1200.00, "quantity": 1, "date": date(2024, 3, 2)},
    {"id": 49, "title": "Отопление", "cost": 3000.00, "quantity": 1, "date": date(2024, 3, 3)},
    {"id": 50, "title": "Вывоз мусора", "cost": 400.00, "quantity": 1, "date": date(2024, 3, 4)},
    {"id": 51, "title": "Онлайн-курс", "cost": 15000.00, "quantity": 1, "date": date(2024, 3, 5)},
    {"id": 52, "title": "Книги по программированию", "cost": 3500.00, "quantity": 3, "date": date(2024, 3, 6)},
    {"id": 53, "title": "Визит к врачу", "cost": 2000.00, "quantity": 1, "date": date(2024, 3, 7)},
    {"id": 54, "title": "Лекарства", "cost": 1200.00, "quantity": 1, "date": date(2024, 3, 8)},
    {"id": 55, "title": "Витамины", "cost": 800.00, "quantity": 2, "date": date(2024, 3, 9)},
    {"id": 56, "title": "Джинсы", "cost": 3000.00, "quantity": 1, "date": date(2024, 3, 10)},
    {"id": 57, "title": "Кроссовки", "cost": 5000.00, "quantity": 1, "date": date(2024, 3, 11)},
    {"id": 58, "title": "Куртка зимняя", "cost": 12000.00, "quantity": 1, "date": date(2024, 3, 12)},
    {"id": 59, "title": "Рубашка", "cost": 2500.00, "quantity": 2, "date": date(2024, 3, 13)},
    {"id": 60, "title": "Авиабилеты", "cost": 25000.00, "quantity": 2, "date": date(2024, 3, 14)},
    {"id": 61, "title": "Отель", "cost": 15000.00, "quantity": 1, "date": date(2024, 3, 15)},
    {"id": 62, "title": "Экскурсия", "cost": 5000.00, "quantity": 1, "date": date(2024, 3, 16)},
    {"id": 63, "title": "Подарок на день рождения", "cost": 3000.00, "quantity": 1, "date": date(2024, 3, 17)},
    {"id": 64, "title": "Цветы", "cost": 1500.00, "quantity": 1, "date": date(2024, 3, 18)},
    {"id": 65, "title": "Бумага для принтера", "cost": 400.00, "quantity": 5, "date": date(2024, 3, 19)},
    {"id": 66, "title": "Ручки", "cost": 200.00, "quantity": 10, "date": date(2024, 3, 20)},
    {"id": 67, "title": "Блокнот", "cost": 300.00, "quantity": 3, "date": date(2024, 3, 21)},
    {"id": 68, "title": "Краска для стен", "cost": 2500.00, "quantity": 3, "date": date(2024, 3, 22)},
    {"id": 69, "title": "Обои", "cost": 4000.00, "quantity": 10, "date": date(2024, 3, 23)},
    {"id": 70, "title": "Инструменты", "cost": 8000.00, "quantity": 1, "date": date(2024, 3, 24)},
    {"id": 71, "title": "Краски для рисования", "cost": 1200.00, "quantity": 1, "date": date(2024, 3, 25)},
    {"id": 72, "title": "Фотоаппарат", "cost": 45000.00, "quantity": 1, "date": date(2024, 3, 26)},
    {"id": 73, "title": "Велосипед", "cost": 25000.00, "quantity": 1, "date": date(2024, 3, 27)},
    {"id": 74, "title": "Удочка", "cost": 3000.00, "quantity": 1, "date": date(2024, 3, 28)},
    {"id": 75, "title": "Горшки для цветов", "cost": 500.00, "quantity": 5, "date": date(2024, 3, 29)},
    {"id": 76, "title": "Земля для растений", "cost": 300.00, "quantity": 3, "date": date(2024, 3, 30)},
    {"id": 77, "title": "Садовый инвентарь", "cost": 4500.00, "quantity": 1, "date": date(2024, 3, 31)},
    {"id": 78, "title": "Корм для кошки", "cost": 1500.00, "quantity": 1, "date": date(2024, 4, 1)},
    {"id": 79, "title": "Наполнитель для туалета", "cost": 800.00, "quantity": 2, "date": date(2024, 4, 2)},
    {"id": 80, "title": "Визит к ветеринару", "cost": 2500.00, "quantity": 1, "date": date(2024, 4, 3)},
    {"id": 81, "title": "Стрижка", "cost": 1000.00, "quantity": 1, "date": date(2024, 4, 4)},
    {"id": 82, "title": "Косметика", "cost": 2500.00, "quantity": 1, "date": date(2024, 4, 5)},
    {"id": 83, "title": "Салон красоты", "cost": 3500.00, "quantity": 1, "date": date(2024, 4, 6)},
    {"id": 84, "title": "Спортивная форма", "cost": 4000.00, "quantity": 1, "date": date(2024, 4, 7)},
    {"id": 85, "title": "Гантели", "cost": 3000.00, "quantity": 2, "date": date(2024, 4, 8)},
    {"id": 86, "title": "Коврик для йоги", "cost": 1500.00, "quantity": 1, "date": date(2024, 4, 9)},
    {"id": 87, "title": "Игрушки", "cost": 2000.00, "quantity": 3, "date": date(2024, 4, 10)},
    {"id": 88, "title": "Одежда для ребенка", "cost": 3500.00, "quantity": 1, "date": date(2024, 4, 11)},
    {"id": 89, "title": "Канцелярия для школы", "cost": 1500.00, "quantity": 1, "date": date(2024, 4, 12)},
    {"id": 90, "title": "Билеты в театр", "cost": 2000.00, "quantity": 2, "date": date(2024, 4, 13)},
    {"id": 91, "title": "Музей", "cost": 800.00, "quantity": 2, "date": date(2024, 4, 14)},
    {"id": 92, "title": "Фотоальбом", "cost": 1200.00, "quantity": 1, "date": date(2024, 4, 15)},
    {"id": 93, "title": "Рамочки для фото", "cost": 500.00, "quantity": 5, "date": date(2024, 4, 16)},
    {"id": 94, "title": "Зонт", "cost": 1500.00, "quantity": 1, "date": date(2024, 4, 17)},
    {"id": 95, "title": "Сумка", "cost": 3000.00, "quantity": 1, "date": date(2024, 4, 18)},
    {"id": 96, "title": "Ремень", "cost": 1200.00, "quantity": 1, "date": date(2024, 4, 19)},
    {"id": 97, "title": "Часы наручные", "cost": 8000.00, "quantity": 1, "date": date(2024, 4, 20)},
    {"id": 98, "title": "Очки солнцезащитные", "cost": 3500.00, "quantity": 1, "date": date(2024, 4, 21)},
    {"id": 99, "title": "Кошелек", "cost": 2000.00, "quantity": 1, "date": date(2024, 4, 22)},
    {"id": 100, "title": "Портмоне", "cost": 2500.00, "quantity": 1, "date": date(2024, 4, 23)},
        ]
        
        for data in initial_fixtures:
            data["user_id"] = 1 
            expense = ExpenseItem(**data)
            self.expenses[expense.id] = expense
            self.next_id = max(self.next_id, expense.id + 1)
    
    def get_all(self, user_id: int = None) -> List[ExpenseItem]:
        if user_id:
            return [expense for expense in self.expenses.values() if expense.user_id == user_id]
        return list(self.expenses.values())
    
    def get_by_id(self, expense_id: int, user_id: int = None) -> Optional[ExpenseItem]:
        expense = self.expenses.get(expense_id)
        if expense and user_id and expense.user_id != user_id:
            return None
        return expense
    
    def create(self, title: str, cost: float, quantity: int, date: date, user_id: int) -> ExpenseItem:
        expense = ExpenseItem(
            id=self.next_id,
            title=title,
            cost=cost,
            quantity=quantity,
            date=date,
            user_id=user_id
        )
        self.expenses[expense.id] = expense
        self.next_id += 1
        return expense
    
    def delete(self, expense_id: int, user_id: int = None) -> bool:
        expense = self.expenses.get(expense_id)
        if expense and (not user_id or expense.user_id == user_id):
            del self.expenses[expense_id]
            return True
        return False
    
    def update(self, expense_id: int, user_id: int = None, **kwargs) -> Optional[ExpenseItem]:
        expense = self.get_by_id(expense_id, user_id)
        if not expense:
            return None
        if 'title' in kwargs and kwargs['title'] is not None:
            expense.title = kwargs['title']
        
        if 'cost' in kwargs and kwargs['cost'] is not None:
            expense.cost = kwargs['cost']
        
        if 'quantity' in kwargs and kwargs['quantity'] is not None:
            expense.quantity = kwargs['quantity']
        
        if 'date' in kwargs and kwargs['date'] is not None:
            expense.date = kwargs['date']
        
        return expense

    def create_expense_db(self, title: str, cost: float, quantity: int, expense_date: date) -> ExpenseModel:
        db = self.SessionLocal()
        expense = ExpenseModel(title=title, cost=cost, quantity=quantity, date=expense_date)
        db.add(expense)
        db.commit()
        db.refresh(expense)
        db.close()
        return expense
    
    def get_expense_db(self, expense_id: int) -> Optional[ExpenseModel]:
        db = self.SessionLocal()
        expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
        db.close()
        return expense
    
    def update_expense_db(self, expense_id: int, **kwargs) -> Optional[ExpenseModel]:
        db = self.SessionLocal()
        expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
        if expense:
            for key, value in kwargs.items():
                if hasattr(expense, key) and value is not None:
                    setattr(expense, key, value)
            db.commit()
            db.refresh(expense)
        db.close()
        return expense
    
    def delete_expense_db(self, expense_id: int) -> bool:
        db = self.SessionLocal()
        expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
        if expense:
            db.delete(expense)
            db.commit()
            db.close()
            return True
        db.close()
        return False
    
    def get_all_expenses_db(self) -> List[ExpenseModel]:
        db = self.SessionLocal()
        expenses = db.query(ExpenseModel).all()
        db.close()
        return expenses

db = Database()