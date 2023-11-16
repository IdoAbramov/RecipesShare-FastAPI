from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from app.src.auth.oauth2 import oauth2
from app.src.auth.AuthRepository import AuthRepository
from app.src.auth import AuthUtils, AuthModels, AuthExceptions, AuthConstants

class AuthServices():

    def __init__(self):
        self.auth_repo = AuthRepository()

    def login_service(self, user_creds: OAuth2PasswordRequestForm) -> str:
        user = self.auth_repo.get_user_data_by_username(user_creds.username)

        if not user:
            raise AuthExceptions.InvalidCredentials()
        
        if not AuthUtils.verify(user_creds.password, user.password):
            login_counter = self.auth_repo.get_login_attempts_counter(user.username)
            if login_counter >= AuthConstants.MAX_ATTEMPTS:
                raise AuthExceptions.TooManyLoginAttempts()
            
            self.auth_repo.increase_login_attempts_counter(username=user.username)
            raise AuthExceptions.InvalidCredentials()
        
        access_token = oauth2.create_access_token(data={"user_id":user.id})
        self.auth_repo.delete_login_attempts(user_creds.username)
        return access_token

    def logout_service(self, access_token: str) -> None:
        blacklist_token = AuthModels.TokensBlacklist(access_token=access_token)
        self.auth_repo.create_blacklist_token_data(blacklist_token)