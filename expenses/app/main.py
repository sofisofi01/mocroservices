from fastapi import FastAPI
from expenses import router as expenses_router
from expenses_es import router as expenses_es_router
from fastapi.middleware.cors import CORSMiddleware
from saga.consumer import start_saga_consumer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expenses_router)
app.include_router(expenses_es_router)

@app.on_event("startup")
def startup():
    start_saga_consumer()