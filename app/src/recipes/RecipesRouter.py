from fastapi import APIRouter, Depends, status,  Response, File, UploadFile
from typing import List
from app.src.recipes import RecipesConstants, RecipesSchemas
from app.src.users import UsersModels
from app.src.auth.oauth2 import oauth2
from app.src.recipes.RecipesServices import RecipesServices

router = APIRouter(tags=["Recipes"], prefix="/api/recipes")

@router.get("", 
            status_code=status.HTTP_200_OK, 
            response_model=List[RecipesSchemas.RecipeData])
async def get_all_recipes(skip: int = RecipesConstants.SKIP_DEFAULT,
                          limit: int = RecipesConstants.LIMIT_DEFAULT,
                          current_user: UsersModels.User = Depends(oauth2.get_current_user)) -> List[RecipesSchemas.RecipeData]:
    recipes = RecipesServices().get_all_recipes_service(skip, limit)
    return recipes

@router.get("/{recipe_id}", 
            status_code=status.HTTP_200_OK,
            response_model=RecipesSchemas.RecipeData)
async def get_recipe_by_id(recipe_id: int,
                           current_user: UsersModels.User = Depends(oauth2.get_current_user)) -> RecipesSchemas.RecipeData:
    recipe = RecipesServices().get_recipe_by_id_service(recipe_id)
    return recipe

@router.get("/users/me",
            status_code=status.HTTP_200_OK,
            response_model=List[RecipesSchemas.RecipeData])
async def get_current_user_recipes(skip: int = RecipesConstants.SKIP_DEFAULT,
                                   limit: int = RecipesConstants.LIMIT_DEFAULT,
                                   current_user: UsersModels.User = Depends(oauth2.get_current_user)) -> List[RecipesSchemas.RecipeData]:
    recipes = RecipesServices().get_recipes_by_user_id_service(current_user.id, limit, skip)
    return recipes

@router.get("/users/{user_id}",
            status_code=status.HTTP_200_OK, 
            response_model=List[RecipesSchemas.RecipeData])
async def get_recipes_by_user(user_id: int, 
                              skip: int = RecipesConstants.SKIP_DEFAULT,
                              limit: int = RecipesConstants.LIMIT_DEFAULT,
                              current_user: UsersModels.User = Depends(oauth2.get_current_user)) -> List[RecipesSchemas.RecipeData]:
    recipes = RecipesServices().get_recipes_by_user_id_service(user_id, limit, skip)
    return recipes

@router.get("/tags/{tag}",
            status_code=status.HTTP_200_OK, 
            response_model=List[RecipesSchemas.RecipeData])
async def get_recipes_by_tag(tag: str,                               
                             skip: int = RecipesConstants.SKIP_DEFAULT,
                             limit: int = RecipesConstants.LIMIT_DEFAULT, 
                             current_user: UsersModels.User = Depends(oauth2.get_current_user)) -> List[RecipesSchemas.RecipeData]:
    recipes = RecipesServices().get_recipes_by_tag_service(tag, limit, skip)
    return recipes

@router.post("", 
             status_code=status.HTTP_201_CREATED, 
             response_model=RecipesSchemas.RecipeData)
async def create_recipe(recipe: RecipesSchemas.RecipeCreate, 
                        current_user: UsersModels.User = Depends(oauth2.get_current_user)) -> RecipesSchemas.RecipeData:
    new_recipe = RecipesServices().create_new_recipe_service(recipe, current_user.id)
    return new_recipe

@router.put("", 
            status_code=status.HTTP_200_OK,
            response_model=RecipesSchemas.RecipeData)
async def update_recipe(recipe: RecipesSchemas.RecipeUpdate,
                        current_user: UsersModels.User = Depends(oauth2.get_current_user)) -> RecipesSchemas.RecipeData:
    updated_recipe = RecipesServices().update_recipe_service(recipe, current_user.id)
    return updated_recipe

@router.delete("/{recipe_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(recipe_id: int,
                        current_user: UsersModels.User = Depends(oauth2.get_current_user)) -> Response:
    recipe_id = RecipesServices().delete_recipe_service(recipe_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 
                    #content=f"Recipe with id <{recipe_id}> deleted successfully.")
