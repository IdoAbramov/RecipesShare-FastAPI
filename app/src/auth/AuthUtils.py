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

"""
def is_admin(current_user: UsersModels.User, 
             db: Session = Depends(database.get_db)) -> bool:
    user = db.query(UsersModels.User).filter(UsersModels.User.id==current_user.id).first()
    if user.role_id == AuthConstants.ADMIN:
        return True
    return False
"""