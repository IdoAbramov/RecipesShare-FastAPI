from fastapi import APIRouter, Response
from fastapi import status, Depends, APIRouter
from app.src.reviews import ReviewsConstants, ReviewsSchemas
from app.src.users import UsersModels
from app.src.reviews.ReviewsServices import ReviewsServices
from app.src.auth.oauth2 import oauth2
from typing import List

router = APIRouter(tags=["Reviews"], prefix="/api/reviews")

@router.get("/recipes/{recipe_id}", 
            response_model=List[ReviewsSchemas.ReviewData])
async def get_recipe_reviews(recipe_id: int,
                             skip: int = ReviewsConstants.SKIP_DEFAULT,
                             limit: int = ReviewsConstants.LIMIT_DEFAULT,
                             current_user: UsersModels.User = Depends(oauth2.get_current_user)):
    reviews_list = ReviewsServices().get_all_recipe_reviews_service(recipe_id, limit, skip)
    return reviews_list

@router.get("/recipes/{recipe_id}/users/{user_id}", 
            response_model=ReviewsSchemas.ReviewData)
async def get_recipe_review_by_user(user_id: int, recipe_id: int, 
                                    current_user: UsersModels.User = Depends(oauth2.get_current_user)):
     review = ReviewsServices().get_recipe_review_by_user_id_service(user_id, recipe_id)
     return review

@router.post("/recipes", 
             status_code=status.HTTP_201_CREATED,
             response_model=ReviewsSchemas.ReviewData)
async def create_recipe_review(review: ReviewsSchemas.ReviewCreate,
                               current_user: UsersModels.User = Depends(oauth2.get_current_user)):
     new_review = ReviewsServices().create_new_review_service(review, current_user.id)
     return new_review

@router.put("/recipes", 
            status_code=status.HTTP_200_OK, 
            response_model=ReviewsSchemas.ReviewData)
async def update_recipe_review_by_id(review: ReviewsSchemas.ReviewUpdate, 
                                     current_user: UsersModels.User = Depends(oauth2.get_current_user)):
     updated_review = ReviewsServices().update_review_service(current_user.id, review)
     return updated_review    

@router.delete("/recipes")
async def delete_recipe_review_by_id(review: ReviewsSchemas.ReviewDelete, 
                                     current_user: UsersModels.User = Depends(oauth2.get_current_user)):
     ReviewsServices().delete_review_service(current_user.id, review.recipe_id)          
     return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/recipes/{recipe_id}/average-rating", 
            response_model=ReviewsSchemas.ReviewAverageRating)
async def get_recipe_average_rating(recipe_id: int, 
                                    current_user: UsersModels.User = Depends(oauth2.get_current_user)):
     average_rating = ReviewsServices().get_average_rating_service(recipe_id)
     return average_rating
