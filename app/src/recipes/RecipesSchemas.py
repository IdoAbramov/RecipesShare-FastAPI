from typing import List
from pydantic import BaseModel, Field
from app.src.users import UsersSchemas

##### Ingredients #####
class IngredientBase(BaseModel):
    name: str
    amount: str
    unit: str

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(IngredientBase):
    pass

class IngredientData(IngredientBase):
    pass

##### Instructions #####
class InstructionBase(BaseModel):
    text: str = Field(min_length=5)

class InstructionCreate(InstructionBase):
    pass

class InstructionUpdate(InstructionBase):
    pass

class InstructionData(InstructionBase):
    step: int

##### Tags #####
class TagBase(BaseModel):
    tag: str

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class TagData(TagBase):
    pass

##### Recipes #####
class RecipeBase(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    additional_text: str = Field(min_length=5, max_length=400)

class RecipeCreate(RecipeBase):
    ingredients: List[IngredientCreate]
    instructions: List[InstructionCreate]
    tags: List[TagCreate]

class RecipeData(RecipeBase):
    id: int
    ingredients: List[IngredientData]
    instructions: List[InstructionData]
    tags: List[TagData]
    owner: UsersSchemas.UserReturn

class RecipeUpdate(RecipeBase):
    id: int
    ingredients: List[IngredientUpdate]
    instructions: List[InstructionUpdate]
    tags: List[TagUpdate]
    
class RecipeDelete(BaseModel):
    id: int