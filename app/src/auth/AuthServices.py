from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from app.src.auth.oauth2 import oauth2
from app.src.auth.AuthRepository import AuthRepository
from app.src.auth import AuthUtils, AuthModels, AuthExceptions

class AuthServices():

    def __init__(self):
        pass

    def login_service(self, user_creds: OAuth2PasswordRequestForm) -> str:
        auth_repo = AuthRepository()
        user = auth_repo.get_user_data_by_username(user_creds.username)

        if not user:
            raise AuthExceptions.InvalidCredentials()
        
        if not AuthUtils.verify(user_creds.password, user.password):
            raise AuthExceptions.InvalidCredentials()
        
        access_token = oauth2.create_access_token(data={"user_id":user.id})
    
        return access_token

    def logout_service(self, access_token: str) -> None:
        auth_repo = AuthRepository()
        blacklist_token = AuthModels.TokensBlacklist(access_token=access_token)
        auth_repo.create_blacklist_token_data(blacklist_token)