import pytest
from fastapi.testclient import TestClient
from app.src.main import app
from app.src import database
from app.src.auth.oauth2 import oauth2
from app.src.recipes import RecipesModels, RecipesUtils
from app.src import init_db

@pytest.fixture(scope="session")
def clear_db():
    database.Base.metadata.drop_all(bind=database.engine)
    database.Base.metadata.create_all(bind=database.engine)
    init_db.initialize_database()

########## First Client User ##########
@pytest.fixture(scope="session")
def client(clear_db):
    yield TestClient(app)

@pytest.fixture(scope="session")
def test_user(client):
    user_data = {"username":"test_create_1", 
                 "password":"123456123123", 
                 "email":"test_create_1@gmail.com",
                 "first_name":"test_1",
                 "last_name":"test_1",
                 "news_registered":"True"}
    
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture(scope="session")
def token(test_user):
    return oauth2.create_access_token({"user_id": test_user["id"]})

@pytest.fixture(scope="session")
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
