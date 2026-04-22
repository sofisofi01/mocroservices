from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import router as auth_router
from saga.router import router as saga_router
from saga.consumer import start_saga_consumer
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

app = FastAPI()

@app.post("/auth/token")
async def proxy_token(form_data: OAuth2PasswordRequestForm = Depends()):
    from auth import login_for_access_token
    return login_for_access_token(form_data)

@app.get("/auth/health", status_code=HTTPStatus.OK)
def health_check():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(saga_router, dependencies=[Depends(oauth2_scheme)])

@app.on_event("startup")
async def startup():
    start_saga_consumer()