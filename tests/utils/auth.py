from sqlalchemy.orm import Session

from models import User
from security.auth import generate_token


def create_autenticate_user(session: Session):
    user = User(name="john", email="john@test.com", admin=True, password="123456")

    session.add(user)
    session.commit()
    session.refresh(user)

    token = generate_token(user.id)

    return token
