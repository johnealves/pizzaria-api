from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from main import oauth2_schema, SECREAT_KEY, ALGORITHM
from db.dependency import get_session
from jose import jwt, JWTError
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
            detail=f'Invalid token'
        )
    
    user = session.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )

    return user