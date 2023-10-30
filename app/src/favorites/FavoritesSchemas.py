from pydantic import BaseModel
from app.src.recipes.RecipesSchemas import RecipeData

class FavoriteData(BaseModel):
    user_id: int
    recipe_id: int
    recipe: RecipeData

class FavoriteCreate(BaseModel):
    recipe_id: int

class FavoriteDelete(BaseModel):
    recipe_id: int