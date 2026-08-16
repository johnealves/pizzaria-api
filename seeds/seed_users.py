from sqlalchemy.orm import Session

from models import User
from security.config import password_hash

from .users import users


def seed_users(session: Session):
    if session.query(User).count() > 0:
        print("Usuarios ja cadastrados")
        return

    db_users = []

    for user in users:
        user_data = user.copy()

        user_data["password"] = password_hash.hash(
            str(user_data["password"])
        )

        db_users.append(User(**user_data))

    session.add_all(db_users)
    session.commit()

    print("Usuarios cadastrados com sucesso")