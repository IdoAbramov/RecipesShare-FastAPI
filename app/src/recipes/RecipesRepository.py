from typing import List
from sqlalchemy import exc, or_
from sqlalchemy.orm import Session
from app.src import database
from app.src.recipes import RecipesModels, RecipesSchemas, RecipesExceptions

class RecipesRepository():

    def __init__(self):
        self.db: Session = database.get_db().__next__()

    def get_tag_data(self, tag: str):
        tag = self.db.query(RecipesModels.Tag).filter(RecipesModels.Tag.tag==tag).first()
        return tag

    def get_all_recipes_data(self, limit: int, skip: int) -> List[RecipesModels.Recipe]:
        recipes = self.db.query(RecipesModels.Recipe).limit(limit).offset(skip).all()
        return recipes

    def create_new_recipe_data(self, new_recipe: RecipesModels.Recipe) -> RecipesModels.Recipe:
        try:
            self.db.add(new_recipe)
            self.db.commit()
            self.db.refresh(new_recipe)

        except exc.IntegrityError:
            raise RecipesExceptions.RecipeDatabaseError()
        return new_recipe

    def get_recipe_data_by_id(self, recipe_id: int) -> RecipesModels.Recipe:
        recipe = self.db.query(RecipesModels.Recipe).filter(RecipesModels.Recipe.id==recipe_id).first()
        return recipe

    def get_recipes_data_by_user_id(self, user_id: int, limit: int, skip: int) -> List[RecipesModels.Recipe]:  
        recipes = self.db.query(RecipesModels.Recipe).filter(
            RecipesModels.Recipe.owner_id==user_id).limit(limit).offset(skip).all()
        return recipes

    def get_recipes_data_by_tag(self, tag: str, limit: int, skip: int) -> List[RecipesModels.Recipe]:
        recipes = self.db.query(RecipesModels.Recipe).join(
            RecipesModels.Tag, RecipesModels.Recipe.id==RecipesModels.Tag.recipe_id).filter(
            RecipesModels.Tag.tag==tag.lower()).limit(limit).offset(skip).all()
        return recipes

    def update_recipe_data(self, 
                           recipe: RecipesModels.Recipe, 
                           ingredients: List[RecipesModels.Ingredient],
                           instructions: List[RecipesModels.Instruction],
                           tags: List[RecipesModels.Tag]) -> RecipesModels.Recipe:

        recipe_update = self.get_recipe_data_by_id(recipe.id)
        try:
            # Update Recipe's basic data
            recipe_update.title = recipe.title
            recipe_update.additional_text = recipe.additional_text
            
            # Update Ingredients
            self.db.query(RecipesModels.Ingredient).filter(RecipesModels.Ingredient.recipe_id==recipe.id).delete()
            self.db.add_all(ingredients)

            # Update Instructions
            self.db.query(RecipesModels.Instruction).filter(RecipesModels.Instruction.recipe_id==recipe.id).delete()
            self.db.add_all(instructions)
            
            # Update tags
            self.db.query(RecipesModels.Tag).filter(RecipesModels.Tag.recipe_id==recipe.id).delete()
            self.db.add_all(tags)

            self.db.commit()
            self.db.refresh(recipe_update)

        except exc.SQLAlchemyError:
            raise RecipesExceptions.RecipeDatabaseError()
        
        return recipe_update

    def delete_recipe_data(self, recipe_id: int) -> None:
        recipe_query = self.db.query(RecipesModels.Recipe).filter(
            RecipesModels.Recipe.id == recipe_id)
        recipe_ingredients_query = self.db.query(RecipesModels.Ingredient).filter(
            RecipesModels.Ingredient.recipe_id == recipe_id)
        recipe_instructions_query = self.db.query(RecipesModels.Instruction).filter(
            RecipesModels.Instruction.recipe_id == recipe_id)
        recipe_tags_query = self.db.query(RecipesModels.Tag).filter(
            RecipesModels.Tag.recipe_id == recipe_id)
        
        try:
            recipe_ingredients_query.delete()
            recipe_instructions_query.delete()
            recipe_tags_query.delete()
            recipe_query.delete()
            self.db.commit()

        except exc.SQLAlchemyError as e:
            print(e)
            raise RecipesExceptions.RecipeDatabaseError()
    
    def get_recipes_data_by_search_expression(self, 
                                              expression: str) -> List[RecipesModels.Recipe]:
        recipes = self.db.query(
            RecipesModels.Recipe
        ).join(
            RecipesModels.Ingredient, RecipesModels.Recipe.id == RecipesModels.Ingredient.recipe_id
        ).join(
            RecipesModels.Tag, RecipesModels.Recipe.id == RecipesModels.Tag.recipe_id
        ).filter(
            or_(
                (RecipesModels.Recipe.title.like(f'%{expression}%')),
                (RecipesModels.Recipe.additional_text.like(f'%{expression}%')),
                (RecipesModels.Ingredient.name.like(f'%{expression}%')),
                (RecipesModels.Tag.tag.like(f'%{expression}%'))
                )
        ).distinct().all()

        return recipes
