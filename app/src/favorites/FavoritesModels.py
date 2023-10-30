from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer
from app.src.database import Base
from sqlalchemy.orm import relationship
from app.src.recipes import RecipesModels
from app.src.users import UsersModels
from sqlalchemy.sql.expression import text

class Favorite(Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user = relationship(UsersModels.User)
    recipe = relationship(RecipesModels.Recipe)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
