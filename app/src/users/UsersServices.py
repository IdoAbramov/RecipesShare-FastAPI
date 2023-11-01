from typing import List
from app.src.users.UsersRepository import UsersRepository
from app.src.users import UsersSchemas, UsersModels, UsersExceptions
from app.src.auth import AuthUtils

class UsersServices():

    def __init__(self):
        self.users_repo = UsersRepository()

    def get_all_users_service(self, 
                              limit: int, 
                              skip: int) -> List[UsersModels.User]:
        users = self.users_repo.get_all_users_data(limit, skip)
        return users

    def get_user_by_id_service(self, 
                               user_id: int) -> UsersModels.User:
        user = self.users_repo.get_user_data_by_id(user_id)
        if not user:
            raise UsersExceptions.UserNotFound(user_id)
        return user

    def create_new_user_service(self, 
                                user: UsersSchemas.UserCreate) -> UsersModels.User:
        hashed_password = AuthUtils.hash(user.password)
        user.password = hashed_password
        model_user = UsersModels.User(**user.model_dump())
        new_user = self.users_repo.create_new_user_data(model_user)
        return new_user

    def update_exist_user_service(self, 
                                  user: UsersSchemas.UserUpdate, 
                                  user_id: int) -> UsersModels.User:
        updated_user = self.users_repo.update_exist_user_data(user, user_id)
        return updated_user