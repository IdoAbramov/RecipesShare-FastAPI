from typing import List
from app.src.follows.FollowsRepository import FollowsRepository
from app.src.follows import FollowsModels, FollowsExceptions
from app.src.recipes.RecipesServices import RecipesServices
from app.src.users import UsersModels

class FollowsServices():

    def __init__(self):
        pass

    def get_all_user_followers_service(self, 
                                       user_id: int, 
                                       limit: int, 
                                       skip: int) -> List[UsersModels.User]:
        follows_repo = FollowsRepository()
        users_list = follows_repo.get_all_user_followers_data(user_id, limit, skip)
        if users_list == []:
            raise FollowsExceptions.FollowersNotFound(user_id)
        return users_list

    def get_all_user_followings_service(self, 
                                        user_id: int, 
                                        limit: int, 
                                        skip: int) -> List[UsersModels.User]:
        follows_repo = FollowsRepository()
        users_list = follows_repo.get_all_user_followings_data(user_id, limit, skip)
        if users_list == []:
            raise FollowsExceptions.FollowingNotFound(user_id)
        return users_list

    def get_all_user_followings_tags_service(self, 
                                             user_id: int, 
                                             limit: int, 
                                             skip: int) -> dict[str, list]:
        follows_repo = FollowsRepository()
        tags = follows_repo.get_all_user_followings_tags_data(user_id, limit, skip)
        if not tags:
            raise FollowsExceptions.TagsFollowingNotFound(user_id)
        
        tags_list = []
        for tag in tags:
            tags_list.append(tag.tag)
        tags_result = dict(tags = tags_list)
        return tags_result

    def create_new_follow_user_service(self, 
                                       current_user_id: int, 
                                       follow_user_id: int) -> None:
        follows_repo = FollowsRepository()
        if current_user_id == follow_user_id:
            raise FollowsExceptions.SelfFollowError(current_user_id)
        is_exist = follows_repo.get_user_follow_record(current_user_id, follow_user_id)
        if is_exist:
            raise FollowsExceptions.UserFollowAlreadyExist(current_user_id, follow_user_id)
        
        new_user_follow = FollowsModels.UserFollow(user_id=current_user_id, follow_user_id=follow_user_id)
        follows_repo.create_new_follow_user_data(new_user_follow)

    def delete_exist_follow_user_service(self, 
                                         current_user_id: int, 
                                         follow_user_id: int) -> None:
        follows_repo = FollowsRepository()
        is_exist = follows_repo.get_user_follow_record(current_user_id, follow_user_id)
        if not is_exist:
            raise FollowsExceptions.UserFollowNotFound(current_user_id, follow_user_id)
        
        follows_repo.delete_exist_follow_user_data(current_user_id, follow_user_id)

    def create_new_follow_tag_service(self, 
                                      current_user_id: int, 
                                      tag: str) -> None:
        follows_repo = FollowsRepository()
        is_exist = RecipesServices().get_tag_record_service(tag) # raises an error if not found
        is_exist = follows_repo.validate_tag_follow_exist(current_user_id, tag)
        if is_exist:
            raise FollowsExceptions.TagFollowAlreadyExist(current_user_id, tag)
        
        new_tag_follow = FollowsModels.TagFollow(user_id=current_user_id, tag=tag.lower())
        follows_repo.create_new_follow_tag_data(new_tag_follow)

    def delete_exist_follow_tag_service(self, 
                                        current_user_id: int, 
                                        tag: str) -> None:
        follows_repo = FollowsRepository()
        is_exist = follows_repo.validate_tag_follow_exist(current_user_id, tag)
        if not is_exist:
            raise FollowsExceptions.TagFollowNotFound(current_user_id, tag)
        
        follows_repo.delete_exist_follow_tag_data(current_user_id, tag)