from fastapi import status
import pytest


def test_create_new_favorite(authorized_client):
    response = authorized_client.post("/api/favorites/recipes", json={"recipe_id":2})
    #print(response.json())
    assert response.status_code == status.HTTP_201_CREATED

def test_get_current_user_favorites(authorized_client):
    response = authorized_client.get("/api/favorites/recipes/me")
    #print(response.json())
    assert response.status_code == status.HTTP_200_OK

def test_delete_exist_favorite(authorized_client):
    response = authorized_client.delete("/api/favorites/recipes/2")
    #print(response.json())
    assert response.status_code == status.HTTP_204_NO_CONTENT
    