from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.src.users import UsersModels
from fastapi import Depends
from app.src.auth import AuthConstants

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)