import os
from typing import Generator

from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import pytest

from main import app
from db.base import Base
from db.dependency import get_session
from models import User, Order, OrderItem, Product


BASE_DIR = Path(__file__).resolve().parent
TEST_DATABASE_URL = f"sqlite:///{BASE_DIR}/banco_test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def session() -> Generator[Session, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

def override_get_session():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
    