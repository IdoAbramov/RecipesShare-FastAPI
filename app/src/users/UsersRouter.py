from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.src.users import UsersConstants, UsersModels, UsersSchemas
from app.src.users.UsersServices import UsersServices
from app.src import database
from app.src.auth.oauth2 import oauth2
from typing import List

router = APIRouter(tags=["Users"], prefix="/api/users")

@router.get("", 
            status_code=status.HTTP_200_OK, 
            response_model=List[UsersSchemas.UserReturn])
async def get_all_users(skip: int = UsersConstants.SKIP_DEFAULT,
                        limit: int = UsersConstants.LIMIT_DEFAULT,
                        current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    users = UsersServices().get_all_users_service(limit, skip)
    return users

@router.get("/me", 
            status_code=status.HTTP_200_OK, 
            response_model=UsersSchemas.UserReturn)
async def get_current_user(current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    user = UsersServices().get_user_by_id_service(current_user.id)
    return user

@router.get("/{user_id}",
            status_code=status.HTTP_200_OK,
            response_model=UsersSchemas.UserReturn)
async def get_user_by_id(user_id: int,
                         current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    user = UsersServices().get_user_by_id_service(user_id)
    return user

@router.post("",
            status_code=status.HTTP_201_CREATED,
            response_model=UsersSchemas.UserReturn)
async def create_new_user(user: UsersSchemas.UserCreate):
    new_user = UsersServices().create_new_user_service(user)
    return new_user

@router.put("/me", 
            response_model=UsersSchemas.UserReturn)
async def update_user_info(user: UsersSchemas.UserUpdate,
                           current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    user_to_update = UsersServices().update_exist_user_service(user, current_user.id)
    return user_to_update

