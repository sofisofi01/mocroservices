from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from expenses import router as expenses_router
from expenses_es import router as expenses_es_router
from fastapi.middleware.cors import CORSMiddleware
from saga.consumer import start_saga_consumer

api_key_header = APIKeyHeader(name="Authorization")

app = FastAPI()

app.include_router(expenses_router, dependencies=[Depends(api_key_header)])

app.include_router(expenses_es_router)

@app.on_event("startup")
def startup():
    start_saga_consumer()