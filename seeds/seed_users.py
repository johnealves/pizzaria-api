from sqlalchemy.orm import Session

from models import User

from .users import users

def seed_users(session: Session):
    if session.query(User).count() > 0:
        print("Usuarios ja cadastrados")
        return

    session.add_all(User(**user) for user in users)
    session.commit()