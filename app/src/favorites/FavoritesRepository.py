from typing import List
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.src import database
from app.src.favorites import FavoritesModels, FavoritesSchemas, FavoritesExceptions
from app.src.recipes import RecipesModels

class FavoritesRepository():

    def __init__(self):
        self.db: Session = database.get_db().__next__()

    def get_user_recpie_favorite_data(self, 
                                      user_id: int, 
                                      recipe_id: int) -> FavoritesModels.Favorite:
        favorite_exist = self.db.query(FavoritesModels.Favorite).filter(
            FavoritesModels.Favorite.recipe_id==recipe_id, 
            FavoritesModels.Favorite.user_id==user_id).first()
        return favorite_exist

    def get_all_user_favorites_data(self, 
                                    user_id: int, 
                                    limit: int, 
                                    skip: int) -> List[FavoritesModels.Favorite]:
        favorite_recipes = self.db.query(RecipesModels.Recipe).join(
            FavoritesModels.Favorite, FavoritesModels.Favorite.recipe_id==RecipesModels.Recipe.id).filter(
                FavoritesModels.Favorite.user_id==user_id).limit(limit).offset(skip).all()
        return favorite_recipes

    def create_new_user_favorite_recipe_data(self, 
                                             favorite: FavoritesModels.Favorite) -> None:
        try:
            self.db.add(favorite)
            self.db.commit()
        except exc.SQLAlchemyError:
            self.db.rollback()
            raise FavoritesExceptions.FavoritesDatabaseError()

    def delete_exist_favorite_recipe_data(self, 
                                          user_id: int, 
                                          recipe_id: int) -> None:
        favorite_query = self.db.query(FavoritesModels.Favorite).filter(
            FavoritesModels.Favorite.recipe_id==recipe_id, 
            FavoritesModels.Favorite.user_id==user_id)              
        try:
            favorite_query.delete()
            self.db.commit()
        
        except exc.SQLAlchemyError:
            self.db.rollback()
            raise FavoritesExceptions.FavoritesDatabaseError()
