from fastapi import FastAPI
from auth import router as auth_router
from saga.router import router as saga_router
from saga.consumer import start_saga_consumer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(saga_router)

@app.on_event("startup")
def startup():
    start_saga_consumer()