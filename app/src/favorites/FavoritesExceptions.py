from fastapi import HTTPException, status

class FavoritesNotFound(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"No favorites for user with id <{user_id}>")
        
class FavoriteAlreadyExist(HTTPException):
    def __init__(self, user_id: int, recipe_id: int):
        super().__init__(status_code=status.HTTP_409_CONFLICT, 
                         detail=f"User with id <{user_id}> already added recipe with id <{recipe_id}> to its favorites")
        
class FavoriteNotExist(HTTPException):
    def __init__(self, user_id: int, recipe_id: int):
        super().__init__(status_code=status.HTTP_409_CONFLICT, 
                         detail=f"User with id <{user_id}> has no recipe with id <{recipe_id}> in its favorites")
        
class FavoritesDatabaseError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                         detail=f"Unable to perform action on favorite due to DB Error")
