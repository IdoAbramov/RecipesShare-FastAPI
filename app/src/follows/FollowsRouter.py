from fastapi import Response, status, Depends, APIRouter
from app.src.follows import FollowsConstants, FollowsSchemas
from app.src.users import UsersSchemas
from app.src.users import UsersModels
from app.src.auth.oauth2 import oauth2
from typing import List
from app.src.follows.FollowsServices import FollowsServices

router = APIRouter(tags=["Follows"], prefix="/api/follows")

# Returns a list of users following the user_id.
@router.get("/users/{user_id}/followers",
            response_model=List[UsersSchemas.UserReturn])
async def get_user_followers(user_id: int,
                             skip: int = FollowsConstants.SKIP_DEFAULT,
                             limit: int = FollowsConstants.LIMIT_DEFAULT,                              
                             current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    users_list = FollowsServices().get_all_user_followers_service(user_id, limit, skip)
    return users_list

# Returns a list of users followed by the user_id.
@router.get("/users/{user_id}/following", 
            response_model=List[UsersSchemas.UserReturn])
async def get_user_followings(user_id: int, 
                              skip: int = FollowsConstants.SKIP_DEFAULT,
                              limit: int = FollowsConstants.LIMIT_DEFAULT,
                              current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    users_list = FollowsServices().get_all_user_followings_service(user_id, limit, skip)
    return users_list
    
# Returns a list of tags followed by the user_id.
@router.get("/users/{user_id}/tags-following")
async def get_tags_followings(user_id: int, 
                             skip: int = FollowsConstants.SKIP_DEFAULT,
                             limit: int = FollowsConstants.LIMIT_DEFAULT,                              
                             current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    tags_list = FollowsServices().get_all_user_followings_tags_service(user_id, limit, skip)
    return tags_list

@router.post("/users")
async def follow_user(follow_user: FollowsSchemas.UserFollowCreate, 
                      current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    FollowsServices().create_new_follow_user_service(current_user.id, follow_user.user_id)
    return Response(status_code=status.HTTP_200_OK, 
    content=f"User with id <{current_user.id}> successfully follows user with id <{follow_user.user_id}>")

@router.delete("/users")
async def unfollow_user(follow_user: FollowsSchemas.UserFollowDelete,
                        current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    FollowsServices().delete_exist_follow_user_service(current_user.id, follow_user.user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@router.post("/tags")
async def follow_tag(tag: FollowsSchemas.TagFollowCreate, 
                     current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    FollowsServices().create_new_follow_tag_service(current_user.id, tag.name)
    return Response(status_code=status.HTTP_200_OK, 
                    content=f"User with id <{current_user.id}> successfully follows tag:{tag.name}.")

@router.delete("/tags")
async def unfollow_tag(tag: FollowsSchemas.TagFollowDelete,
                       current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    FollowsServices().delete_exist_follow_tag_service(current_user.id, tag.name)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

