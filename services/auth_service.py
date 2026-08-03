from datetime import timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models import User
from schemas.auth_schemas import LoginResponse, LoginSchema
from schemas.user_schemas import UserActionResponse, UserSchema
from security.auth import generate_token
from security.config import password_hash


class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def user_authetication(
        self,
        email: str,
        password: str,
    ) -> User | None:
        user: User = self.session.query(User).filter(User.email == email).first()

        if not user or not password_hash.verify(password, user.password):
            return False
        else:
            return user

    def create(self, user: UserSchema) -> UserActionResponse:
        selected_user = (
            self.session.query(User).filter(User.email == user.email).first()
        )

        if selected_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User email already exists",
            )
        else:
            crypted_password = password_hash.hash(user.password)
            new_user = User(
                name=user.name,
                email=user.email,
                password=crypted_password,
                active=user.active,
                admin=user.admin,
            )
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            return {
                "message": "User created successfully",
                "user": new_user,
            }

    def login(self, login: LoginSchema) -> LoginResponse:
        user: User = self.user_authetication(login.email, login.password)

        if not user:
            raise HTTPException(
                status_code=404, detail="user not found or incorrect password"
            )

        access_token = generate_token(user.id)
        refresh_token = generate_token(user.id, timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }

    def login_form(self, form_data: OAuth2PasswordRequestForm):
        user: User = self.user_authetication(form_data.username, form_data.password)

        if not user:
            raise HTTPException(
                status_code=404, detail="user not found or incorrect password"
            )
        else:
            access_token = generate_token(user.id)
            return {"access_token": access_token, "token_type": "Bearer"}

    def refresh_token(self, user):
        access_token = generate_token(user.id)
        return {"access_token": access_token, "token_type": "Bearer"}
