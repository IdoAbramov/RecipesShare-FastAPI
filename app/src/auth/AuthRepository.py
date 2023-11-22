from typing import List
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.src import database
from app.src.users import UsersModels
from app.src.auth import AuthModels, AuthExceptions, AuthSchemas
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

    def get_login_attempts_counter(self, username: str):
        login_attempts = self.db.query(
            AuthModels.LoginAttempts).filter(
                AuthModels.LoginAttempts.username==username).first()
        if not login_attempts:
            return 0
        return login_attempts.counter

    def increase_login_attempts_counter(self, username: str):
        counter = self.get_login_attempts_counter(username)
        counter += 1
        
        try:
            if counter == 1:
                self.db.add(AuthModels.LoginAttempts(username=username, counter=counter))
            else:
                login_attempt = AuthSchemas.LoginAttempts(username=username, counter=counter)
                user_attempts_query = self.db.query(
                    AuthModels.LoginAttempts).filter(
                        AuthModels.LoginAttempts.username==username)
                user_attempts_query.update(login_attempt.model_dump(),
                                           synchronize_session=False)
            self.db.commit()

        except:
            self.db.rollback()
            raise AuthExceptions.AuthDatabaseError()

    def delete_login_attempts(self, username: str):
        user_attempts_query = self.db.query(
                    AuthModels.LoginAttempts).filter(
                        AuthModels.LoginAttempts.username==username)
        try:
            user_attempts_query.delete()
            self.db.commit()
        except:
            raise AuthExceptions.AuthDatabaseError()