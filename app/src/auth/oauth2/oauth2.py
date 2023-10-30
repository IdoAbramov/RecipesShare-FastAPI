from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer 
from sqlalchemy.orm import Session
from app.src.config import settings
from app.src.auth import AuthSchemas, AuthModels
from app.src.users import UsersModels
from app.src import database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire}) # it will take the current time + the time to expire and put it here. 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, creds_exception, db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")
        if id is None:
            raise creds_exception
        token_data = AuthSchemas.TokenData(id=id)
    except JWTError:
        raise creds_exception
    
    blacklist_token = db.query(AuthModels.TokensBlacklist).filter(AuthModels.TokensBlacklist.access_token == token).first()
    if blacklist_token != None:
        raise creds_exception

    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), 
                     db: Session = Depends(database.get_db)):
    creds_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                    detail="Could not verify token", 
                                    headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, creds_exception, db)
    user = db.query(UsersModels.User).filter(UsersModels.User.id == token.id).first()
    return user
