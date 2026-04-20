import json
import os
import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from kafka import KafkaProducer
from crypt import CryptService
from saga.events import TOPIC, MONTH_CLOSE_REQUESTED
from saga.consumer import saga_results
from schema_registry import schema_client

router = APIRouter(prefix="/saga", tags=["saga"])

SAGA_SCHEMA = {
    "type": "object",
    "properties": {
        "event_type": {"type": "string"},
        "saga_id": {"type": "string"},
        "user_id": {"type": "integer"},
        "year": {"type": "integer"},
        "month": {"type": "integer"}
    },
    "required": ["event_type", "saga_id", "user_id", "year", "month"]
}

@router.on_event("startup")
def register_saga_schema():
    schema_client.register_schema(f"{TOPIC}-value", SAGA_SCHEMA)

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
    
    schema_info = schema_client.get_latest_schema(f"{TOPIC}-value")
    schema_id = schema_info.get("id") if schema_info else None

    event_payload = {
        "event_type": MONTH_CLOSE_REQUESTED,
        "saga_id": saga_id,
        "user_id": user_id,
        "year": year,
        "month": month,
    }

    producer = get_producer()
    
    if schema_id:
        import struct
        header = struct.pack(">bI", 0, schema_id)
        data = header + json.dumps(event_payload).encode("utf-8")
        producer.send(TOPIC, data)
    else:
        producer.send(TOPIC, event_payload)
        
    producer.flush()

    return {"saga_id": saga_id, "status": "started"}


@router.get("/close-month/{saga_id}")
def get_saga_status(saga_id: str, user_id: int = Depends(get_current_user)):
    result = saga_results.get(saga_id)
    if not result:
        return {"saga_id": saga_id, "status": "pending"}
    return {"saga_id": saga_id, **result}
