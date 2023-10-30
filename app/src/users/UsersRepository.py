from typing import List
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.src import database
from app.src.users import UsersModels, UsersSchemas, UsersExceptions


class UsersRepository():

    def __init__(self):
        self.db: Session = database.get_db().__next__()

    def get_all_users_data(self, 
                           limit: int, 
                           skip: int) -> List[UsersModels.User]:
        users = self.db.query(UsersModels.User).order_by(
            UsersModels.User.id).limit(limit).offset(skip).all()
        return users
    
    def get_user_data_by_id(self, 
                            user_id: int) -> UsersModels.User:
        user = self.db.query(UsersModels.User).filter(UsersModels.User.id == user_id).first()
        return user
    
    def create_new_user_data(self, 
                             user: UsersModels.User) -> UsersModels.User:
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

        except exc.IntegrityError as e:
            print(e)
            self.db.rollback()
            raise UsersExceptions.UserAlreadyExist()
        
        except exc.SQLAlchemyError as e:
            print(e)
            self.db.rollback()
            raise UsersExceptions.UserDatabaseError()
        
        self.db.close()
        return user

    def update_exist_user_data(self, 
                               exist_user: UsersSchemas.UserUpdate, 
                               user_id: int) -> UsersModels.User:
        user_query = self.db.query(UsersModels.User).filter(UsersModels.User.id == user_id)
        user_to_update = user_query.first()

        try:
            user_query.update(exist_user.model_dump(), synchronize_session=False)
            self.db.commit()
            self.db.refresh(user_to_update)

        except exc.SQLAlchemyError:
            self.db.rollback()
            raise UsersExceptions.UserDatabaseError()
        
        return user_to_update