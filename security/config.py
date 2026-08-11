import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///banco.db')
TEST_DATABASE = os.getenv("TEST_DATABASE", 'false') in ('true', 'yes')
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password_hash = PasswordHash.recommended()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")
