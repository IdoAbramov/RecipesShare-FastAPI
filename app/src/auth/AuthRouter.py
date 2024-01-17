from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.src.auth.oauth2 import oauth2
from app.src.users import UsersModels
from app.src.auth.AuthServices import AuthServices

router = APIRouter(tags=["Authentication"], prefix="/api")


@router.post("/login")
def login(user_creds: OAuth2PasswordRequestForm = Depends()):
    access_token = AuthServices().login_service(user_creds)
    return {"access_token":access_token, "token_type":"bearer"}

@router.post("/logout")
def logout(current_user: UsersModels.User = Depends(oauth2.get_current_user),
           access_token: str = Depends(oauth2.oauth2_scheme)):
    AuthServices().logout_service(access_token)
    return Response(status_code=status.HTTP_200_OK, 
                    content=f"user with id <{current_user.id}> logged out successfully.")