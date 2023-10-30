from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.src import database
from app.src.users import UsersModels
from app.src.follows import FollowsModels, FollowsExceptions

class FollowsRepository():

    def __init__(self):
        self.db: Session = database.get_db().__next__()

    def get_user_follow_record(self, user_id: int, follow_user_id: int):
        follow_record = self.db.query(FollowsModels.UserFollow).filter(
            FollowsModels.UserFollow.user_id==user_id, FollowsModels.UserFollow.follow_user_id==follow_user_id).first()
        return follow_record
    
    def validate_tag_follow_exist(self, user_id: int, follow_tag: str):
        follow_record = self.db.query(FollowsModels.TagFollow).filter(
            FollowsModels.TagFollow.user_id==user_id, FollowsModels.TagFollow.tag==follow_tag).first()
        return follow_record

    def get_all_user_followers_data(self, user_id: int, limit: int, skip: int):
        users_list = self.db.query(UsersModels.User).join(
            FollowsModels.UserFollow, UsersModels.User.id==FollowsModels.UserFollow.user_id).filter(
            FollowsModels.UserFollow.follow_user_id==user_id).limit(limit).offset(skip).all()
        return users_list

    def get_all_user_followings_data(self, user_id: int, limit: int, skip: int):
        users_list = self.db.query(UsersModels.User).join(
            FollowsModels.UserFollow, UsersModels.User.id==FollowsModels.UserFollow.follow_user_id).filter(
            FollowsModels.UserFollow.user_id==user_id).limit(limit).offset(skip).all()
        return users_list

    def get_all_user_followings_tags_data(self, user_id: int, limit: int, skip: int):
        tags = self.db.query(FollowsModels.TagFollow).filter(
            FollowsModels.TagFollow.user_id==user_id).limit(limit).offset(skip).all()
        return tags

    def create_new_follow_user_data(self, new_user_follow: FollowsModels.UserFollow):
        try:
            self.db.add(new_user_follow)
            self.db.commit()
        except exc.SQLAlchemyError:
            self.db.rollback()
            raise FollowsExceptions.FollowDatabaseError()
        
    def delete_exist_follow_user_data(self, current_user_id: int, follow_user_id: int):        
        follow_query = self.db.query(FollowsModels.UserFollow).filter(
            FollowsModels.UserFollow.user_id==current_user_id, 
            FollowsModels.UserFollow.follow_user_id==follow_user_id)
        try:
            follow_query.delete()
            self.db.commit()
        except exc.SQLAlchemyError:
            self.db.rollback()
            raise FollowsExceptions.FollowDatabaseError()
        
    def create_new_follow_tag_data(self, new_tag_follow: FollowsModels.TagFollow):
        try:
            self.db.add(new_tag_follow)
            self.db.commit()
        except exc.SQLAlchemyError:
            self.db.rollback()
            raise FollowsExceptions.FollowDatabaseError()
        
    def delete_exist_follow_tag_data(self, current_user_id: int, tag: str):
        follow_query = self.db.query(FollowsModels.TagFollow).filter(
                        FollowsModels.TagFollow.user_id==current_user_id, 
                        FollowsModels.TagFollow.tag==tag)
        try:
            follow_query.delete()
            self.db.commit()
        
        except exc.SQLAlchemyError:
            self.db.rollback()
            raise FollowsExceptions.FollowDatabaseError()