from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from app.src.database import Base
from app.src.auth import AuthConstants

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    is_active = Column(Boolean, nullable=False, server_default='false')
    news_registered = Column(Boolean, nullable=False, server_default='false')
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, server_default=str(AuthConstants.RoleID.REGULAR.value))
