from typing import List
from app.src.reviews import ReviewsSchemas, ReviewsModels, ReviewsUtils, ReviewsExceptions
from app.src.reviews.ReviewsRepository import ReviewsRepository
from app.src.recipes.RecipesServices import RecipesServices

class ReviewsServices():

    def __init__(self):
        self.reviews_repo = ReviewsRepository()
    
    def get_all_recipe_reviews_service(self, 
                                       recipe_id: int, 
                                       limit: int, 
                                       skip: int) -> List[ReviewsModels.Review]:
        reviews = self.reviews_repo.get_all_recipe_reviews_data(recipe_id, limit, skip)
        if not reviews:
            raise ReviewsExceptions.RecipeReviewsNotFound(recipe_id)
        return reviews

    def get_recipe_review_by_user_id_service(self, 
                                             user_id: int, 
                                             recipe_id: int) -> ReviewsModels.Review:
        review = self.reviews_repo.get_recipe_review_data_by_user_id(user_id, recipe_id)
        if not review:
            raise ReviewsExceptions.UserReviewNotFound(recipe_id, user_id)
        return review

    def get_average_rating_service(self, 
                                   recipe_id: int) -> ReviewsSchemas.ReviewAverageRating:
        review_exist = self.reviews_repo.is_recipe_reviewed(recipe_id)
        if review_exist == None:
            raise ReviewsExceptions.RecipeReviewsNotFound(recipe_id)
        avg_rating = self.reviews_repo.get_recipe_average_rating_data(recipe_id)
        avg_rating_schema = ReviewsSchemas.ReviewAverageRating(average_rating=avg_rating)        
        return avg_rating_schema

    def create_new_review_service(self, 
                                  review: ReviewsSchemas.ReviewCreate, 
                                  user_id: int) -> ReviewsModels.Review:
        recipe = RecipesServices().get_recipe_by_id_service(review.recipe_id) # raises an error if not found
                
        if recipe.owner_id == user_id:
            raise ReviewsExceptions.SelfReviewError(user_id)
        
        review_exist = self.reviews_repo.get_recipe_review_data_by_user_id(user_id, review.recipe_id)
        if review_exist:
            raise ReviewsExceptions.ReviewAlreadyExist(review.recipe_id, user_id)

        is_valid_review_data = ReviewsUtils.validate_review_data(review)
        if not is_valid_review_data:
            raise ReviewsExceptions.InvalidReviewData(review.recipe_id, user_id)
        
        review_model = ReviewsModels.Review(user_id=user_id, 
                                            **review.model_dump())

        new_review = self.reviews_repo.create_new_recipe_review_data(review_model, user_id)
        return new_review

    def update_review_service(self, 
                              current_user_id: int, 
                              review: ReviewsSchemas.ReviewUpdate) -> ReviewsModels.Review:

        is_valid_review_data = ReviewsUtils.validate_review_data(review)
        if not is_valid_review_data:
            raise ReviewsExceptions.InvalidReviewData(review.recipe_id, current_user_id)
        
        review_exist = self.reviews_repo.get_recipe_review_data_by_user_id(current_user_id, review.recipe_id)
        if not review_exist:
            raise ReviewsExceptions.UserReviewNotFound(review.recipe_id, current_user_id)

        updated_review = self.reviews_repo.update_exist_recipe_review_data(review, current_user_id)

        return updated_review
    
    def delete_review_service(self, current_user_id: int, recipe_id: int) -> None:
        review_exist = self.reviews_repo.get_recipe_review_data_by_user_id(current_user_id, recipe_id)
        if not review_exist:
            raise ReviewsExceptions.UserReviewNotFound(recipe_id, current_user_id)
        self.reviews_repo.delete_exist_recipe_review_data(recipe_id, current_user_id)


