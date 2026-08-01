from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from db.dependency import get_session
from models import User
from schemas.schemas import LoginSchema, UserSchema
from security.auth import generate_token, get_current_user
from security.config import (
    password_hash,
)
from services.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def home():
    return {"message": "Authentication endpoint", "authenticated": False}


@auth_router.post("/create_user")
async def create_user(user: UserSchema, session=Depends(get_session)):
    existing_user = session.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User email already exists")
    else:
        crypted_password = password_hash.hash(user.password)
        new_user = User(
            name=user.name,
            email=user.email,
            password=crypted_password,
            active=user.active,
            admin=user.admin,
        )
        session.add(new_user)
        session.commit()
        return {
            "message": "User created successfully",
            "user": {"name": new_user.name, "email": new_user.email},
        }


@auth_router.post("/login")
async def login(login: LoginSchema, session=Depends(get_session)):

    user: User = AuthService(session).user_authetication(login.email, login.password, session)

    if not user:
        raise HTTPException(
            status_code=404, detail="user not found or incorrect password"
        )
    else:
        access_token = generate_token(user.id)
        refresh_token = generate_token(user.id, timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }


@auth_router.post("/login-form")
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)
):
    user: User = AuthService(session).user_authetication(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(
            status_code=404, detail="user not found or incorrect password"
        )
    else:
        access_token = generate_token(user.id)
        return {"access_token": access_token, "token_type": "Bearer"}


@auth_router.get("/refresh_token")
async def use_refresh_token(user: User = Depends(get_current_user)):
    access_token = generate_token(user.id)
    return {"access_token": access_token, "token_type": "Bearer"}
