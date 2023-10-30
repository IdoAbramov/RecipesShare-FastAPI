from . import RecipesModels, RecipesSchemas, RecipesUtils, RecipesExceptions
from typing import List
from .RecipesRepository import RecipesRepository


class RecipesServices():

    def __init__(self):
        pass

    def get_all_recipes_service(self, 
                                skip: int, 
                                limit: int) -> List[RecipesModels.Recipe]:
        recipes_repo = RecipesRepository()
        recipes = recipes_repo.get_all_recipes_data(limit, skip)
        return recipes

    def create_new_recipe_service(self, 
                                  recipe: RecipesSchemas.RecipeCreate, 
                                  user_id: int) -> RecipesModels.Recipe:
        recipes_repo = RecipesRepository()
        new_recipe_record = RecipesModels.Recipe(
                                title=recipe.title,
                                additional_text=recipe.additional_text,

                                ingredients=[RecipesModels.Ingredient(**ingredient.model_dump()) \
                                    for ingredient in recipe.ingredients],

                                instructions=[RecipesModels.Instruction(**instruction.model_dump()) \
                                    for instruction in RecipesUtils.enumerate_instructions_steps(recipe.instructions)],

                                tags=[RecipesModels.Tag(**tag.model_dump()) \
                                    for tag in RecipesUtils.parse_tags_list(recipe.tags)],

                                owner_id = user_id)
        
        recipe_created = recipes_repo.create_new_recipe_data(new_recipe_record)
        return recipe_created
    
    def get_recipe_by_id_service(self, 
                                 recipe_id: int) -> RecipesModels.Recipe:
        recipes_repo = RecipesRepository()
        recipe = recipes_repo.get_recipe_data_by_id(recipe_id)
        if not recipe:
            raise RecipesExceptions.RecipeNotFound(recipe_id)
        return recipe

    def get_recipes_by_user_id_service(self, 
                                       user_id: int, 
                                       limit: int, 
                                       skip: int) -> List[RecipesModels.Recipe]:
        recipes_repo = RecipesRepository()
        recipes = recipes_repo.get_recipes_data_by_user_id(user_id, limit, skip)
        if not recipes:
            raise RecipesExceptions.UserRecipesNotFound(user_id)
        return recipes

    def get_recipes_by_tag_service(self, 
                                   tag: str, 
                                   limit: int, 
                                   skip: int) -> List[RecipesModels.Recipe]:
        recipes_repo = RecipesRepository()
        recipes = recipes_repo.get_recipes_data_by_tag(tag, limit, skip)
        if not recipes:
            raise RecipesExceptions.UserRecipesNotFound(tag)
        return recipes

    def update_recipe_service(self, 
                              recipe: RecipesSchemas.RecipeUpdate, 
                              current_user_id: int) -> RecipesModels.Recipe:
        recipes_repo = RecipesRepository()
        recipe_to_update = recipes_repo.get_recipe_data_by_id(recipe.id)
        if not recipe_to_update:
            raise RecipesExceptions.RecipeNotFound(recipe.id)
        RecipesUtils.validate_user_owner(recipe_to_update, current_user_id)
                
        ingredients = [RecipesModels.Ingredient(recipe_id=recipe.id,**ingredient.model_dump()) \
                        for ingredient in recipe.ingredients]
        
        instructions = [RecipesModels.Instruction(recipe_id=recipe.id,**instruction.model_dump()) \
                        for instruction in RecipesUtils.enumerate_instructions_steps(recipe.instructions)]
        
        tags = [RecipesModels.Tag(recipe_id=recipe.id,**tag.model_dump()) \
                         for tag in RecipesUtils.parse_tags_list(recipe.tags)]

        recipe_updated = recipes_repo.update_recipe_data(recipe, ingredients, instructions, tags)

        return recipe_updated
    
    def delete_recipe_service(self, 
                              recipe_id: int, 
                              current_user_id: int) -> int:
        recipes_repo = RecipesRepository()
        recipe_to_delete = recipes_repo.get_recipe_data_by_id(recipe_id)
        if not recipe_to_delete:
            raise RecipesExceptions.RecipeNotFound(recipe_id)
        
        RecipesUtils.validate_user_owner(recipe_to_delete, current_user_id)

        recipes_repo.delete_recipe_data(recipe_id)
        return recipe_to_delete.id
    
    def get_tag_record_service(self, 
                               tag: str):
        recipes_repo = RecipesRepository()
        tag_model = recipes_repo.get_tag_data(tag)
        if not tag_model:
            RecipesExceptions.TagNotFound(tag)
        return tag_model
