import os
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
TOKEN_EXPIRE_MINUTES = 60

class CryptService:

    @staticmethod
    def decode_token(token: str) -> str:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            login = payload.get("sub")
            if not login:
                raise ValueError("Invalid token payload")
            return login
        except jwt.JWTError:
            raise ValueError("Invalid token")