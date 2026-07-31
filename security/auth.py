from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone

from db.dependency import get_session
from models.user_models import User
from security.config import (
    ALGORITHM,
    SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    oauth2_schema,
    password_hash
)

def user_authetication(
    email: str, password: str, session: Session = Depends(get_session)
):
    user: User = session.query(User).filter(User.email == email).first()

    if not user or not password_hash.verify(password, user.password):
        return False
    else:
        return user

def generate_token(
    user_id: str, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
):
    expiration_date = datetime.now(timezone.utc) + duration_token
    dict_info = {"sub": str(user_id), "exp": expiration_date}
    encode_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encode_jwt

def get_current_user(
    token: str = Depends(oauth2_schema), session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token.")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )

    return user
