import os
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = os.getenv("SECRET_KEY")
TOKEN_EXPIRE_MINUTES = 60

class CryptService:

    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_hashed_password(cls, password: str) -> str:
        return cls.context.hash(password)
    
    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return cls.context.verify(password, hashed_password)

    @staticmethod
    def create_token(login: str) -> str:
        claims = {
            "sub": login,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(claims, SECRET_KEY, algorithm="HS256")