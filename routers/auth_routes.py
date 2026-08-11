from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from db.dependency import get_session
from models import User
from schemas.auth_schemas import LoginResponse, LoginSchema
from schemas.user_schemas import UserActionResponse, UserSchema
from security.auth import get_current_user
from services.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


# @auth_router.get("/")
# async def home():
#     return {"message": "Authentication endpoint", "authenticated": False}


@auth_router.post(
    "/create_user",
    response_model=UserActionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: UserSchema, session=Depends(get_session)):
    return AuthService(session).create(user)


@auth_router.post("/login", response_model=LoginResponse)
async def login(login: LoginSchema, session=Depends(get_session)):
    return AuthService(session).login(login)


@auth_router.post("/login-form")
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)
):
    return AuthService(session).login_form(form_data)


@auth_router.get("/refresh_token")
async def use_refresh_token(
    user: User = Depends(get_current_user), session=Depends(get_session)
):
    return AuthService(session).refresh_token(user)
