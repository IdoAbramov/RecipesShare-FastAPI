from typing import List
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.src import database
from app.src.users import UsersModels
from app.src.auth import AuthModels, AuthExceptions
from app.src.users import UsersModels

class AuthRepository():

    def __init__(self):
        self.db: Session = database.get_db().__next__()

    def get_user_data_by_username(self, username: str) -> UsersModels.User:
        user = self.db.query(UsersModels.User).filter(
                UsersModels.User.username == username).first()
        return user
    
    def create_blacklist_token_data(self, blacklist_token: AuthModels.TokensBlacklist) -> None:
        try:
            self.db.add(blacklist_token)
            self.db.commit()
        except exc.SQLAlchemyError:
            self.db.rollback()
            raise AuthExceptions.AuthDatabaseError()
