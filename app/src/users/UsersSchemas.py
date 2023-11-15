from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=10)
    password: str = Field(min_length=10)
    email: EmailStr
    first_name: str
    last_name: str
    news_registered: Optional[bool]

class UserUpdate(BaseModel):
    first_name:str
    last_name:str
    news_registered: Optional[bool]

class UserDelete(BaseModel):
    id: int
    
class UserReturn(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        from_attributes = True