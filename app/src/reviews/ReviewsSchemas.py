from pydantic import BaseModel
from app.src.users.UsersSchemas import UserReturn

class ReviewBase(BaseModel):
    rating: int
    text: str
        
class ReviewData(ReviewBase):
    recipe_id: int
    user_id: int
    owner: UserReturn

class ReviewCreate(ReviewBase):
    recipe_id: int

class ReviewUpdate(ReviewBase):
    recipe_id: int

class ReviewDelete(BaseModel):
    recipe_id: int

class ReviewAverageRating(BaseModel):
    average_rating: float

