from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from db.dependency import get_session
from main import ALGORITHM, SECREAT_KEY, oauth2_schema
from models.user_models import User


def get_current_user(
    token: str = Depends(oauth2_schema),
    session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(token, SECREAT_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token."
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail='Invalid token'
        )
    
    user = session.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )

    return user