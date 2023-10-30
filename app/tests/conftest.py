import pytest
from fastapi.testclient import TestClient
from app.src.main import app
from app.src import database
from app.src.auth.oauth2 import oauth2
from app.src.recipes import RecipesModels, RecipesUtils

# Recreates a clean DB
@pytest.fixture(scope="session")
def client():
    database.Base.metadata.drop_all(bind=database.engine)
    database.Base.metadata.create_all(bind=database.engine)
    yield TestClient(app)

@pytest.fixture(scope="session")
def test_user(client):
    user_data = {"username":"test_create_1", 
                 "password":"123456", 
                 "email":"test_create_1@gmail.com",
                 "first_name":"test",
                 "last_name":"test",
                 "news_registered":"True"}
    
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture(scope="session")
def test_user_2(client):
    user_data = {"username":"test_create_2", 
                 "password":"123456", 
                 "email":"test_create_2@gmail.com",
                 "first_name":"test",
                 "last_name":"test",
                 "news_registered":"True"}
    
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

# Creates a token by the new user
@pytest.fixture(scope="session")
def token(test_user):
    return oauth2.create_access_token({"user_id":test_user["id"]})

# Authorize the new user
@pytest.fixture(scope="session")
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client


"""

##### Second user #####
@pytest.fixture(scope="session")
def test_user_2(client):
    user_data = {"username":"test_create_2", 
                 "password":"123456", 
                 "email":"test_create_2@gmail.com",
                 "first_name":"test_2",
                 "last_name":"test_2",
                 "news_registered":"True"}
    
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

# Creates a token by the new user
@pytest.fixture(scope="session")
def token_2(test_user_2):
    return oauth2.create_access_token({"user_id":test_user_2["id"]})

# Authorize the new user
@pytest.fixture(scope="session")
def authorized_client_2(client, token_2):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token_2}"
    }
    return client
"""
"""
@pytest.fixture(scope="session")
def test_recipes():
    recipes_data = [
            {"title":"recipe test #1", 
             "additional_text":"additional text for recipe #1", 
            "ingredients":[
                {"name":"ingredient #1", "amount":"10", "unit":"kg"},
                {"name":"ingredient #2", "amount":"3-5", "unit":"units"}
            ],
            "instructions":[
                {"text":"step #1 here"}, 
                {"text":"step #2 here"}
            ],
            "tags":[
                {"tag":"Tasty"}, 
                {"tag":"random-tag"}, 
                {"tag":"easy-to-do"}
            ],
            "owner_id":1
            }, {"title":"recipe test #2", 
            "additional_text":"a test initial text for recipe #2", 
            "ingredients":[
                {"name":"QWE", "amount":"11", "unit":"grams"},
                {"name":"ASD", "amount":"2", "unit":"units"}
            ],
            "instructions":[
                {"text":"step 1 here as well"}, 
                {"text":"step 2 right after"}
            ],
            "tags":[
                {"tag":"diet"}, 
                {"tag":"hard-recipe"}, 
                {"tag":"baking"}
            ],
            "owner_id":2}
        ]
    
    def create_recipe_model(recipe_data):
        return RecipesModels.Recipe(
                                title=recipe_data["title"],
                                additional_text=recipe_data["additional_text"],

                                ingredients=[RecipesModels.Ingredient(**ingredient) \
                                    for ingredient in recipe_data["ingredients"]],

                                instructions=[RecipesModels.Instruction(**instruction) \
                                    for instruction in RecipesUtils.enumerate_instructions_steps(recipe_data["instructions"])],

                                tags=[RecipesModels.Tag(**tag) \
                                    for tag in RecipesUtils.parse_tags_list(recipe_data["tags"])],

                                owner_id = recipe_data["owner_id"])

    recipes = []
    for recipe in recipes_data:
        recipes.append(create_recipe_model(recipe))
    #recipes_map = map(create_recipe_model, recipes_data)
    #print(recipes_map)
    #recipes = list(recipes_map)
    
    db = database.get_db().__next__()
    db.add_all(recipes)
    db.commit()
    recipes = db.query(RecipesModels.Recipe).all()
    return recipes

"""