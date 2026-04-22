from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models import UserRegister, TokenOut, UserLogin
from database_models import User
from database import db
from crypt import CryptService
from kafka_producer import KafkaService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenOut)
def register(user_data: UserRegister):
    session = db.SessionLocal()
    existing_user = session.query(User).filter(User.login == user_data.login).first()
    if existing_user:
        session.close()
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(
        login=user_data.login,
        hashed_password=CryptService.get_hashed_password(user_data.password[:72])
    )
    session.add(new_user)
    session.flush()
    
    db.add_to_outbox(session, 
        aggregate_id=str(new_user.id),
        aggregate_type='user',
        event_type='user_registered',
        payload={
            'event_type': 'user_registered',
            'login': user_data.login,
            'user_id': new_user.id
        }
    )
    
    session.commit()
    session.refresh(new_user)
    token = CryptService.create_token(user_data.login)
    session.close()
    
    return {"token": token}

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    session = db.SessionLocal()
    user = session.query(User).filter(User.login == form_data.username).first()

    if not user or not CryptService.verify_password(form_data.password, user.hashed_password):
        session.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = CryptService.create_token(user.login)
    session.close()
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=TokenOut)
def login(user_data: UserLogin):
    session = db.SessionLocal()
    login = user_data.login
    password = user_data.password
    user = session.query(User).filter(User.login == login).first()

    if not user or not CryptService.verify_password(password, user.hashed_password):
        session.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db.add_to_outbox(session,
        aggregate_id=str(user.id),
        aggregate_type='user',
        event_type='user_logged_in',
        payload={
            'event_type': 'user_logged_in',
            'login': user.login,
            'user_id': user.id
        }
    )
    
    session.commit()
    token = CryptService.create_token(user.login)
    session.close()

    return {"token": token}