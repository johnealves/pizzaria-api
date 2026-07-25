from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from routers.auth_routes import auth_router
from routers.orders_routes import orders_router

app = FastAPI()
password_hash = PasswordHash.recommended()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

app.include_router(auth_router)
app.include_router(orders_router)

# Para rodar o codigo, executar no terminal uvicorn main:app --reload
