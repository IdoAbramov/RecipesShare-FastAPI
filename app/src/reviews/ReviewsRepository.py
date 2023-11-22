from typing import List
from sqlalchemy import exc, func
from sqlalchemy.orm import Session
from app.src import database
from app.src.reviews import ReviewsSchemas, ReviewsModels, ReviewsExceptions

class ReviewsRepository():

    def __init__(self):
        self.db: Session = database.get_db().__next__()

    def is_recipe_reviewed(self, 
                           recipe_id: int) -> ReviewsModels.Review:
        any_review = self.db.query(ReviewsModels.Review).filter(ReviewsModels.Review.recipe_id==recipe_id).first()
        return any_review

    def get_all_recipe_reviews_data(self, 
                                    recipe_id: int, 
                                    limit: int, 
                                    skip: int) -> List[ReviewsModels.Review]:
        reviews = self.db.query(ReviewsModels.Review).filter(
                    ReviewsModels.Review.recipe_id==recipe_id).limit(limit).offset(skip).all()
        return reviews

    def get_recipe_review_data_by_user_id(self, 
                                          user_id: int, 
                                          recipe_id: int) -> ReviewsModels.Review:
        review = self.db.query(ReviewsModels.Review).filter(
            ReviewsModels.Review.recipe_id==recipe_id, ReviewsModels.Review.user_id==user_id).first()
        return review
    
    def get_recipe_average_rating_data(self, 
                                       recipe_id: int) -> int:
        avg_rating = self.db.query(func.avg(ReviewsModels.Review.rating)).filter(
            ReviewsModels.Review.recipe_id==recipe_id).scalar()
        return avg_rating

    def create_new_recipe_review_data(self, 
                                      review: ReviewsModels.Review,
                                      user_id: int) -> ReviewsModels.Review:        
        try:
            self.db.add(review)
            self.db.commit()
            self.db.refresh(review)

        except exc.SQLAlchemyError:
            self.db.rollback()
            raise ReviewsExceptions.ReviewDatabaseError()
        return review

    def update_exist_recipe_review_data(self,
                                        review: ReviewsSchemas.ReviewUpdate,
                                        user_id: int) -> ReviewsModels.Review:

        review_query = self.db.query(ReviewsModels.Review).filter(
            ReviewsModels.Review.recipe_id==review.recipe_id, 
            ReviewsModels.Review.user_id==user_id)
        review_to_update = review_query.first()
        try:
            review_query.update(review.model_dump(), synchronize_session=False)
            self.db.commit()
            self.db.refresh(review_to_update)

        except exc.SQLAlchemyError:
            self.db.rollback()
            raise ReviewsExceptions.ReviewDatabaseError()

        return review_to_update

    def delete_exist_recipe_review_data(self, recipe_id: int, user_id: int):
        review_query = self.db.query(ReviewsModels.Review).filter(
            ReviewsModels.Review.user_id==user_id, 
            ReviewsModels.Review.recipe_id==recipe_id)
        try:
            review_query.delete()
            self.db.commit()
        
        except exc.SQLAlchemyError:
            self.db.rollback()
            raise ReviewsExceptions.ReviewDatabaseError()
