from app.src.reviews import ReviewsSchemas, ReviewsConstants

def validate_review_data(review: ReviewsSchemas.ReviewData) -> bool:
    return ReviewsConstants.MIN_REVIEW_RATING <= review.rating <= ReviewsConstants.MAX_REVIEW_RATING and \
        ReviewsConstants.MIN_REVIEW_LENGTH <= len(review.text) <= ReviewsConstants.MAX_REVIEW_LENGTH
