from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from app.src.database import Base
from app.src.users.UsersModels import User # for the relationship

class Review(Base):
    __tablename__ = "reviews"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True, nullable=False)
    rating = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=expression.text('now()'))
    owner = relationship("User")
