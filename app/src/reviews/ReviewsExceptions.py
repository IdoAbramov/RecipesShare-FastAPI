from fastapi import HTTPException, status

class RecipeReviewsNotFound(HTTPException):
    def __init__(self, recipe_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"No reviews for recipe with id <{recipe_id}>")

class UserReviewNotFound(HTTPException):
    def __init__(self, recipe_id: int, user_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"No review by user with id <{user_id}> for recipe with id <{recipe_id}>")
        
class ReviewDatabaseError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                         detail=f"Unable to perform action on reviews due to DB Error")

class SelfReviewError(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, 
                         detail=f"User with id <{user_id}> cannot review its own recipe")

class ReviewAlreadyExist(HTTPException):
    def __init__(self, recipe_id: int, user_id: int):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, 
                         detail=f"User with id <{user_id}> already posted review for recipe with id <{recipe_id}>")

class InvalidReviewData(HTTPException):
    def __init__(self, recipe_id: int, user_id: int):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, 
                         detail=f"User with id <{user_id}> review for recipe with id <{recipe_id}> is invalid")
