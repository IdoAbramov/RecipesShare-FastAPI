from fastapi import HTTPException, status

class AuthDatabaseError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                         detail=f"Unable to perform action on authorization due to DB Error")

class InvalidCredentials(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, 
                         detail=f"Invalid Credentials")