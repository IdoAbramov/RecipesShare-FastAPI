from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from app.src.database import Base
from sqlalchemy.sql.expression import text

class UserFollow(Base):
    __tablename__ = "users_follows"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    follow_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class TagFollow(Base):
    __tablename__ = "tags_follows"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    tag = Column(String, primary_key=True, nullable=False)
