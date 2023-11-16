from sqlalchemy import Column, Integer, String
from app.src.database import Base


class TokensBlacklist(Base):
    __tablename__ = "tokens_blacklist"

    id = Column(Integer, primary_key=True, nullable=False)
    access_token = Column(String, nullable=False)
    
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

class LoginAttempts(Base):
    __tablename__ = "login_attempts"

    username = Column(String, primary_key=True, nullable=False, unique=True)
    counter = Column(Integer, nullable=False)