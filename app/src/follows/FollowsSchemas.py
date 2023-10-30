from pydantic import BaseModel

class UserFollowBase(BaseModel):
    user_id: int

class UserFollowCreate(UserFollowBase):
    pass

class UserFollowDelete(UserFollowBase):
    pass

class TagFollowBase(BaseModel):
    name: str

class TagFollowCreate(TagFollowBase):
    pass

class TagFollowDelete(TagFollowBase):
    pass