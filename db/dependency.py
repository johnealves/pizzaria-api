from sqlalchemy.orm import Session, sessionmaker

from .database import db


def get_session():
    try:
        SessionLocal = sessionmaker(bind=db)
        SessionLocal = Session()
        yield SessionLocal
    finally:
        SessionLocal.close()
