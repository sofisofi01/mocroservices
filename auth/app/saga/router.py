import json
import os
import uuid
import uuid
from fastapi import APIRouter, HTTPException, Depends
from database import db
from saga.events import TOPIC, MONTH_CLOSE_REQUESTED

router = APIRouter(prefix="/saga", tags=["saga"])

saga_results = {}

def get_current_user():
    return 1

@router.post("/close-month")
def close_month(year: int, month: int, user_id: int = Depends(get_current_user)):
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Invalid month")

    saga_id = str(uuid.uuid4())
    
    event_payload = {
        "event_type": MONTH_CLOSE_REQUESTED,
        "saga_id": saga_id,
        "user_id": user_id,
        "year": year,
        "month": month,
    }

    session = db.SessionLocal()
    try:
        db.add_to_outbox(session, 
            aggregate_id=saga_id,
            aggregate_type='saga',
            event_type=MONTH_CLOSE_REQUESTED,
            payload=event_payload
        )
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        session.close()

    return {"saga_id": saga_id, "status": "started"}

@router.get("/close-month/{saga_id}")
def get_saga_status(saga_id: str, user_id: int = Depends(get_current_user)):
    result = saga_results.get(saga_id)
    if not result:
        return {"saga_id": saga_id, "status": "pending"}
    return {"saga_id": saga_id, **result}
