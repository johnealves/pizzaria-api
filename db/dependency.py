from sqlalchemy.orm import Session, sessionmaker

from .database import SessionLocal

def get_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
