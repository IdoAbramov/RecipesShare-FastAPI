import pytest
from fastapi.testclient import TestClient
from app.src.main import app
from app.src import database
from app.src.auth.oauth2 import oauth2
from app.src.recipes import RecipesModels, RecipesUtils

@pytest.fixture(scope="session")
def clear_db():
    database.Base.metadata.drop_all(bind=database.engine)
    database.Base.metadata.create_all(bind=database.engine)


########## First Client User ##########
@pytest.fixture(scope="session")
def client_1(clear_db):
    yield TestClient(app)

@pytest.fixture(scope="session")
def test_user_1(client_1):
    user_data = {"username":"test_create_1", 
                 "password":"123456", 
                 "email":"test_create_1@gmail.com",
                 "first_name":"test_1",
                 "last_name":"test_1",
                 "news_registered":"True"}
    
    response = client_1.post("/api/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture(scope="session")
def token_1(test_user_1):
    return oauth2.create_access_token({"user_id":test_user_1["id"]})

@pytest.fixture(scope="session")
def authorized_client_1(client_1, token_1):
    client_1.headers = {
        **client_1.headers,
        "Authorization":f"Bearer {token_1}"
    }
    return client_1

########## Second Client User ##########

@pytest.fixture(scope="session")
def client_2():
    yield TestClient(app)

@pytest.fixture(scope="session")
def test_user_2(client_2):
    user_data = {"username":"test_create_2", 
                 "password":"123456", 
                 "email":"test_create_2@gmail.com",
                 "first_name":"test",
                 "last_name":"test",
                 "news_registered":"True"}
    
    response = client_2.post("/api/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture(scope="session")
def token_2(test_user_2):
    return oauth2.create_access_token({"user_id":test_user_2["id"]})

@pytest.fixture(scope="session")
def authorized_client_2(client_2, token_2):
    client_2.headers = {
        **client_2.headers,
        "Authorization":f"Bearer {token_2}"
    }
    return client_2
