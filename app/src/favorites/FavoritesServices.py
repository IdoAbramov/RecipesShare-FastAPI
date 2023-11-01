from typing import List
from app.src.favorites.FavoritesRepository import FavoritesRepository
from app.src.recipes.RecipesServices import RecipesServices
from app.src.favorites import FavoritesSchemas, FavoritesModels, FavoritesExceptions

class FavoritesServices():

    def __init__(self):
        self.favorites_repo = FavoritesRepository()

    def get_all_favorites_service(self, 
                                  user_id: int, 
                                  limit: int, 
                                  skip: int) -> List[FavoritesModels.Favorite]:
        #favorites_repo = FavoritesRepository()
        favorite_recipes = self.favorites_repo.get_all_user_favorites_data(user_id, limit, skip)
        if not favorite_recipes:
            raise FavoritesExceptions.FavoritesNotFound(user_id)
        return favorite_recipes

    def add_favorite_recipe_service(self, 
                                    favorite: FavoritesSchemas.FavoriteCreate,
                                    user_id: int) -> None:
        favorites_repo = FavoritesRepository()
        recipe_exist = RecipesServices().get_recipe_by_id_service(favorite.recipe_id) # raises an error if not found
        favorite_exist = favorites_repo.get_user_recpie_favorite_data(user_id, recipe_exist.id)
        if favorite_exist:
            raise FavoritesExceptions.FavoriteAlreadyExist(user_id, recipe_exist.id)
        new_favorite = FavoritesModels.Favorite(user_id=user_id, recipe_id=favorite.recipe_id)
        favorites_repo.create_new_user_favorite_recipe_data(new_favorite)

    def remove_favorite_recipe_service(self, 
                                       recipe_id: int,
                                       user_id: int) -> None:
        favorites_repo = FavoritesRepository()
        favorite_exist = favorites_repo.get_user_recpie_favorite_data(user_id, recipe_id)
        if not favorite_exist:
            raise FavoritesExceptions.FavoriteNotExist(user_id, recipe_id)
        favorites_repo.delete_exist_favorite_recipe_data(user_id, recipe_id)