from app.src.recipes import RecipesModels, RecipesSchemas, RecipesExceptions
from typing import List

def validate_user_owner(recipe: RecipesModels.Recipe, user_id: int) -> None:
    if recipe.owner_id != user_id:
        raise RecipesExceptions.InvalidOwnerError(recipe.id, user_id)
    
def tags_delete_duplicates(tags: List[RecipesSchemas.TagData]) -> List[RecipesSchemas.TagData]:
        tags_list = [tag.tag for tag in tags]
        tags_list = list(dict.fromkeys(tags_list))
        new_tags_schemas_list = [RecipesSchemas.TagCreate(tag=tag) for tag in tags_list]
        return new_tags_schemas_list
    
def tags_lowercase(tags: List[RecipesSchemas.TagData]) -> List[RecipesSchemas.TagData]:
        lowercase_tags_list = [tag.tag.lower() for tag in tags]
        new_tags_schemas_list = [RecipesSchemas.TagCreate(tag=tag) for tag in lowercase_tags_list]
        return new_tags_schemas_list
    
def parse_tags_list(tags: List[RecipesSchemas.TagData]) -> List[RecipesSchemas.TagData]:
        return tags_delete_duplicates(tags_lowercase(tags))

def enumerate_instructions_steps(instructions: List[RecipesSchemas.InstructionCreate]) -> RecipesSchemas.InstructionData:
    instructions_list = [RecipesSchemas.InstructionData(step=step, text=instruction.text) \
                        for step, instruction in enumerate(instructions, 1)]    
    return instructions_list        
