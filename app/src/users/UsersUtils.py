from app.src.users import UsersModels, UsersExceptions
from sqlalchemy.orm import Session

def check_user_exist(user_id: int, db: Session):
    user_exist = db.query(UsersModels.User).filter(UsersModels.User.id==user_id).first()
    if not user_exist:
        raise UsersExceptions.UserNotFound(user_id)
