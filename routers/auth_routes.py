from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from db.dependency import get_current_user, get_session
from main import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, password_hash
from models import User
from schemas.schemas import LoginSchema, UserSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def generate_token(user_id: str, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + duration_token
    dict_info = {
        "sub": str(user_id),
        "exp": expiration_date
    }
    encode_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encode_jwt

def user_authetication(email: str, password: str, session: Session = Depends(get_session)):
    user: User = session.query(User).filter(User.email == email).first()

    if not user or not password_hash.verify(password, user.password):
        return False
    else:
        return user

@auth_router.get("/")
async def home():
    return {
        "message": "Authentication endpoint",
        "authenticated": False
    }

@auth_router.post('/create_user')
async def create_user(user: UserSchema, session = Depends(get_session)):
    existing_user = session.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User email already exists")
    else:
        crypted_password = password_hash.hash(user.password)
        new_user = User(name=user.name, email=user.email, password=crypted_password, active=user.active, admin=user.admin)
        session.add(new_user)
        session.commit()
        return {
            "message": "User created successfully",
            "user": {"name": new_user.name, "email": new_user.email}
        }

@auth_router.post('/login')
async def login(login: LoginSchema, session = Depends(get_session)):
    user: User = user_authetication(login.email, login.password, session)

    if not user:
        raise HTTPException(status_code=404, detail="user not found or incorrect password")
    else:
        access_token = generate_token(user.id)
        refresh_token = generate_token(user.id, timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

@auth_router.post("/login-form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session = Depends(get_session)):
    user: User = user_authetication(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(status_code=404, detail="user not found or incorrect password")
    else:
        access_token = generate_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

@auth_router.get('/refresh_token')
async def use_refresh_token(user: User = Depends(get_current_user)):
    access_token = generate_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }