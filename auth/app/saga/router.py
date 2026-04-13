import json
import os
import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from kafka import KafkaProducer
from crypt import CryptService
from saga.events import TOPIC, MONTH_CLOSE_REQUESTED
from saga.consumer import saga_results

router = APIRouter(prefix="/saga", tags=["saga"])
security = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(security)) -> int:
    try:
        user_id = CryptService.decode_token(token)
        if not user_id:
            raise HTTPException(status_code=401, detail="User not found")
        return user_id
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_producer():
    return KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


@router.post("/close-month")
def close_month(year: int, month: int, user_id: int = Depends(get_current_user)):
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month")

    saga_id = str(uuid.uuid4())
    producer = get_producer()
    producer.send(TOPIC, {
        "event_type": MONTH_CLOSE_REQUESTED,
        "saga_id": saga_id,
        "user_id": user_id,
        "year": year,
        "month": month,
    })
    producer.flush()

    return {"saga_id": saga_id, "status": "started"}


@router.get("/close-month/{saga_id}")
def get_saga_status(saga_id: str, user_id: int = Depends(get_current_user)):
    result = saga_results.get(saga_id)
    if not result:
        return {"saga_id": saga_id, "status": "pending"}
    return {"saga_id": saga_id, **result}
