from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from .database import db
from models import User
from main import SECREAT_KEY, ALGORITHM, oauth2_schema
from jose import jwt, JWTError

def get_session():
    try:
        SessionLocal= sessionmaker(bind=db)
        SessionLocal = Session()
        yield SessionLocal
    finally:
        SessionLocal.close()
