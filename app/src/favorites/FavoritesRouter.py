from fastapi import Response, status, Depends, APIRouter
from app.src.favorites import FavoritesConstants, FavoritesSchemas
from app.src.favorites.FavoritesServices import FavoritesServices
from app.src.users import UsersModels
from app.src.recipes import RecipesSchemas
from app.src.auth.oauth2 import oauth2
from typing import List

router = APIRouter(tags=["Favorites"], prefix="/api/favorites")

@router.get("/recipes/me",
            response_model=List[RecipesSchemas.RecipeData],
            status_code=status.HTTP_200_OK)
async def get_current_user_favorites(skip: int = FavoritesConstants.SKIP_DEFAULT,
                                     limit: int = FavoritesConstants.LIMIT_DEFAULT,
                                     current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    favorite_recipes = FavoritesServices().get_all_favorites_service(current_user.id, limit, skip)
    return favorite_recipes

@router.post("/recipes", 
             status_code=status.HTTP_201_CREATED)
async def create_new_favorite(favorite: FavoritesSchemas.FavoriteCreate,
                              current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    print(current_user)
    FavoritesServices().add_favorite_recipe_service(favorite, current_user.id)
    return Response(content=f"Recipe with id <{favorite.recipe_id}> added succssfully to user with id <{current_user.id}> favorites",
                    status_code=status.HTTP_201_CREATED)

@router.delete("/recipes/{recipe_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_exist_favorite(recipe_id: int, 
                                current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    FavoritesServices().remove_favorite_recipe_service(recipe_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
                    #content=f"Recipe with id <{favorite.recipe_id}> removed succssfully from user with id <{current_user.id}> favorites")
