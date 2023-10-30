from fastapi import HTTPException, status

class RecipeDatabaseError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                         detail=f"Unable to perform action on recipes due to DB Error")

class RecipeNotFound(HTTPException):
    def __init__(self, recipe_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"Recipe with id <{recipe_id}> not found")

class UserRecipesNotFound(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"No recipes for user with id <{user_id}>")

class TagRecipesNotFound(HTTPException):
    def __init__(self, tag: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"No recipes for tag <{tag}>")

class TagNotFound(HTTPException):
    def __init__(self, tag: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"Tag <{tag}> not found")
        
class InvalidRecipeOwnerError(HTTPException):
    def __init__(self, recipe_id: int, user_id: int):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, 
                         detail=f"User with id <{user_id}> is not the owner of recipe with id <{recipe_id}>")
