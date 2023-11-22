from fastapi import Depends
from sqlalchemy.orm import Session
from app.src import database
from app.src.auth import AuthConstants, AuthSchemas, AuthModels


def initialize_database():
    db: Session = database.get_db().__next__()
    role = db.query(AuthModels.Role).first()
    if role:
        return

    # Initialize the roles in DB on first time startup
    try:
        admin = AuthModels.Role(id=AuthConstants.RoleID.ADMIN.value,
                                name=AuthConstants.RoleName.ADMIN.value)
        db.add(admin)
        regular = AuthModels.Role(id=AuthConstants.RoleID.REGULAR.value,
                                  name=AuthConstants.RoleName.REGULAR.value)
        db.add(regular)
        db.commit()

    except:
        db.rollback()
