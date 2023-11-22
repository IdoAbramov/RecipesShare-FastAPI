from typing import List
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from app.src.database import Base
from app.src.users.UsersModels import User # for the relationship

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    additional_text = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner = relationship("User")
    ingredients = relationship("Ingredient", back_populates="recipe")
    instructions = relationship("Instruction", back_populates="recipe")
    tags = relationship("Tag", back_populates="recipe")

class Ingredient(Base):
    __tablename__ = "ingredients"
    
    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True, nullable=False)
    name = Column(String, primary_key=True, index=True)
    amount = Column(String)
    unit = Column(String)
    
    recipe = relationship("Recipe", back_populates="ingredients")

class Instruction(Base):
    __tablename__ = "instructions"
    
    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True, nullable=False)
    step = Column(Integer, primary_key=True, index=True, nullable=False) 
    text = Column(String)
    
    recipe = relationship("Recipe", back_populates="instructions")


class Tag(Base):
    __tablename__ = "tags"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True, nullable=False)
    tag = Column(String, primary_key=True, index=True, nullable=False)

    recipe = relationship("Recipe", back_populates="tags")
