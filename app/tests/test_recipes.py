from fastapi import status
import pytest

# Create some recipes
recipes_create_data = [
    ("recipe test #1", 
     "additional text for recipe #1", 
     [
        {"name":"ingredient #1", "amount":"10", "unit":"kg"},
        {"name":"ingredient #2", "amount":"3-5", "unit":"units"}
     ],
     [
         {"text":"step #1 here"}, 
         {"text":"step #2 here"}
     ],
     [
         {"tag":"Tasty"}, 
         {"tag":"random-tag"}, 
         {"tag":"easy-to-do"}
     ]),
     ("recipe test #2", 
     "a test initial text for recipe #2", 
     [
        {"name":"QWE", "amount":"11", "unit":"grams"},
        {"name":"ASD", "amount":"2", "unit":"units"}
     ],
     [
         {"text":"step 1 here as well"}, 
         {"text":"step 2 right after"}
     ],
     [
         {"tag":"diet"}, 
         {"tag":"hard-recipe"}, 
         {"tag":"baking"}
     ])
]

# Will update both recipes
recipes_update_data = [
    (1,
     "recipe test #1 updated", 
     "additional text for recipe #1 updated", 
     [
        {"name":"ingredient #1 updated", "amount":"5", "unit":"kg"},
        {"name":"ingredient #2 updated", "amount":"6-8", "unit":"units"}
     ],
     [
        {"text":"step #1 here updated"}, 
        {"text":"step #2 here updated"},
        {"text":"step #3 here updated"}
     ],
     [
         {"tag":"Tasty-update"}, 
         {"tag":"random-tag"}, 
         {"tag":"easy-to-do"}
     ])
     ,
     (2,
      "recipe test #2 updated", 
      "a test initial text for recipe #2 updated", 
     [
        {"name":"QWE updated", "amount":"4", "unit":"grams updated"},
        {"name":"ASD updated", "amount":"6", "unit":"units updated"}
     ],
     [
         {"text":"step 1 here as well updated"}, 
         {"text":"step 2 right after updated"}
     ],
     [
         {"tag":"diet-update"}, 
         {"tag":"hard-recipe"}
     ])
]

# recipes to delete IDs
recipes_delete_data = [(1)]


@pytest.mark.order(2)
@pytest.mark.parametrize("title, additional_text, ingredients, instructions, tags", 
                         recipes_create_data)
def test_create_new_recipe(authorized_client_1, title, additional_text, ingredients, instructions, tags):
    response = authorized_client_1.post("/api/recipes", json={"title":title,
                                                            "additional_text":additional_text,
                                                            "ingredients":ingredients,
                                                            "instructions":instructions,
                                                            "tags":tags})
    #print(response.json())
    assert response.status_code == status.HTTP_201_CREATED

def test_get_all_recipes(authorized_client_1):
    response = authorized_client_1.get("/api/recipes")
    #print(response.json())
    assert response.status_code == status.HTTP_200_OK

def test_get_recipe_by_id(authorized_client_1):
    response = authorized_client_1.get("/api/recipes/2")
    #print(response.json())
    assert response.status_code == status.HTTP_200_OK

def test_get_current_user_recipes(authorized_client_1):
    response = authorized_client_1.get("/api/recipes/users/me")
    #print(response.json())
    assert response.status_code == status.HTTP_200_OK

def test_get_recipes_by_tag(authorized_client_1):
    response = authorized_client_1.get("/api/recipes/tags/tasty")
    #print(response.json())
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.parametrize("id, title, additional_text, ingredients, instructions, tags", 
                         recipes_update_data)
def test_update_recipe(authorized_client_1, id, title, additional_text, ingredients, instructions, tags):
    response = authorized_client_1.put("/api/recipes", json={"id":id,
                                                           "title":title,
                                                           "additional_text":additional_text,
                                                           "ingredients":ingredients,
                                                           "instructions":instructions,
                                                           "tags":tags})
    #print(response.json())
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.parametrize("id", recipes_delete_data)
def test_delete_recipe(authorized_client_1, id):
    response = authorized_client_1.delete(f"/api/recipes/{id}")
    #print(response.json())
    assert response.status_code == status.HTTP_204_NO_CONTENT

