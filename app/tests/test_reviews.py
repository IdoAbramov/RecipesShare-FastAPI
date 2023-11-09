from fastapi import status
import pytest
from app.src.recipes.RecipesServices import RecipesServices
from app.src.recipes import RecipesSchemas

# To notice and parametrize the: user_id in the service, the recipe_id in the post request
def test_create_recipe_review(authorized_client_1):
    recipe = RecipesSchemas.RecipeCreate(title="recipe test",
                                         additional_text="additional text for recipe",
                                         ingredients=[RecipesSchemas.IngredientCreate(name="test", amount="1", unit="test")],
                                         instructions=[RecipesSchemas.InstructionCreate(text="1 step for test")],
                                         tags=[RecipesSchemas.TagCreate(tag="test")])
    RecipesServices().create_new_recipe_service(recipe, 1)
    response = authorized_client_1.post("/api/reviews/recipes", json={"rating":7, 
                                                                    "text":"just some text to test", 
                                                                    "recipe_id":3})

"""
#recipe_reviews_data = [(2),(1)]

def test_create_recipe_review(authorized_client):
    response = authorized_client.post("/api/reviews/recipes", json={"rating":7, 
                                                                    "text":"just some text to test", 
                                                                    "recipe_id":2})
    print(response)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.parametrize("recipe_id", recipe_reviews_data)
def test_get_recipe_reviews(authorized_client, recipe_id):
    response = authorized_client.get(f"/api/reviews/recipes/{recipe_id}")
    assert response.status_code == status.HTTP_200_OK

def test_get_recipe_review_by_user(authorized_client):
    pass

def test_update_recipe_review(authorized_client):
    pass

def test_delete_recipe_review(authorized_client):
    pass

def test_get_recipe_average_rating(authorized_client):
    pass
    
"""
