from fastapi import HTTPException, status

class UserNotFound(HTTPException):
    def __init__(self, user_id):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"User with id <{user_id}> not found")

class UserAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, 
                         detail="User with the same username or email address is already exists")

class UserDatabaseError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                         detail=f"Unable to perform action on users due to DB Error")
