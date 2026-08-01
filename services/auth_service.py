from sqlalchemy.orm import Session
from models import User
from security.config import password_hash


class AuthService:

    def __init__(self, session: Session):
        self.session = session

    def user_authetication(
        self,
        email: str, password: str,
    ) -> User | bool:
        user: User = self.session.query(User).filter(User.email == email).first()

        if not user or not password_hash.verify(password, user.password):
            return False
        else:
            return user