from fastapi import HTTPException, status

class FollowersNotFound(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"User with id <{user_id}> has no users in followers list")
        
class FollowingNotFound(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"User with id <{user_id}> has no users in following list")

class TagsFollowingNotFound(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"User with id <{user_id}> has no tags in following list")
        
class FollowDatabaseError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                         detail=f"Unable to perform action on follows due to DB Error")

class UserFollowAlreadyExist(HTTPException):
    def __init__(self, user_id, follow_user_id):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, 
                         detail=f"User with id <{user_id}> already follows user with id <{follow_user_id}>")

class UserFollowNotFound(HTTPException):
    def __init__(self, user_id, follow_user_id):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, 
                         detail=f"User with id <{user_id}> not follows user with id <{follow_user_id}>")

class TagFollowAlreadyExist(HTTPException):
    def __init__(self, user_id, tag):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, 
                         detail=f"User with id <{user_id}> already follows tag <{tag}>")

class TagFollowNotFound(HTTPException):
    def __init__(self, user_id, tag):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, 
                         detail=f"User with id <{user_id}> not follows tag <{tag}>")

class SelfFollowError(HTTPException):
    def __init__(self, user_id):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, 
                         detail=f"User with id <{user_id}> cannot follow itself")
