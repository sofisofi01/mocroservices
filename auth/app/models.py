from pydantic import BaseModel, Field
from typing import Annotated

LoginType = Annotated[str, Field(min_length=3, max_length=50)]
PasswordType = Annotated[str, Field(min_length=6, max_length=36)]
TokenType = Annotated[str, Field()]
    
class BaseUser(BaseModel):
    login: LoginType
    password: PasswordType

class UserRegister(BaseUser):
    pass

class UserLogin(BaseUser):
    pass

class TokenOut(BaseModel):
    token: TokenType