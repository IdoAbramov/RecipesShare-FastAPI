from fastapi import status
import pytest
from app.tests import globals

TEST_USERNAME = "create_user_test"
TEST_PASSWORD = "123456123123"

# Tests creation of a new user
@pytest.mark.order(1)
def test_create_new_user(client):
    response = client.post("/api/users",
                           json={"username":TEST_USERNAME, 
                                 "password":TEST_PASSWORD, 
                                 "email":"create_user_test@gmail.com",
                                 "first_name":"test",
                                 "last_name":"test",
                                 "news_registered":"True"})
    print(response.json())
    globals.created_user_id = response.json()["id"]
    assert response.status_code == status.HTTP_201_CREATED

# Tests login user


def test_login(client):
    response = client.post("/api/login",
                           data={"username":TEST_USERNAME, 
                                 "password":TEST_PASSWORD})
    #print(response.json())
    assert response.status_code == status.HTTP_200_OK

def test_get_all_users(authorized_client):
    response = authorized_client.get("/api/users")
    #print(response.json())
    assert response.status_code == status.HTTP_200_OK


def test_get_user_by_id(authorized_client):
    response = authorized_client.get("/api/users/1")
    #print(response.json())
    assert response.status_code == status.HTTP_200_OK


def test_get_current_user(authorized_client):
    response = authorized_client.get("/api/users/me")
    #print(response.json())
    assert response.status_code == status.HTTP_200_OK


def test_update_user_info(authorized_client):
    response = authorized_client.put("/api/users/me", json={"first_name": "updated_test",
                                                             "last_name":"updated_test",
                                                             "news_registered":"False"})
    #print (response.json())
    assert response.status_code == status.HTTP_200_OK