from fastapi.testclient import TestClient
from fastapi import status
from menuapp.main import app
import random
from datetime import datetime

random.seed(datetime.now().timestamp())

client = TestClient(app=app)

"""____________________________MENU_TESTS_____________________________"""

def test_crud_for_menu():
    # Create menu item
    menu_id = 0
    title = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(10))
    desc = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(10))
    response = client.post('/api/v1/menus', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data
    assert type(response_data["title"]) is str
    assert type(response_data["description"]) is str
    assert type(response_data["id"]) is str
    assert type(response_data["submenus_count"]) is int
    assert type(response_data["dishes_count"]) is int
    assert response_data["title"] == title
    assert response_data["description"] == desc
    assert int(response_data["id"]) > 0
    assert response_data["submenus_count"] >= 0
    assert response_data["dishes_count"] >= 0
    menu_id = response_data["id"]

    # Get menu list
    response = client.get('/api/v1/menus')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    for item in response_data:
        assert type(item["title"]) is str
        assert type(item["description"]) is str
        assert type(item["id"]) is str
        assert type(item["submenus_count"]) is int
        assert type(item["dishes_count"]) is int
        assert int(item["id"]) > 0
        assert item["submenus_count"] >= 0
        assert item["dishes_count"] >= 0

    # Get menu item
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert type(response_data["title"]) is str
    assert type(response_data["description"]) is str
    assert type(response_data["id"]) is str
    assert type(response_data["submenus_count"]) is int
    assert type(response_data["dishes_count"]) is int
    assert int(response_data["id"]) > 0
    assert response_data["submenus_count"] >= 0
    assert response_data["dishes_count"] >= 0

    # Get non-existant menu item
    response = client.get('/api/v1/menus/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert type(response_data["detail"]) is str
    assert response_data["detail"] == "menu not found"

    # Update menu item
    title += "1"
    desc += "1"
    response = client.patch(f'/api/v1/menus/{menu_id}', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert type(response_data["title"]) is str
    assert type(response_data["description"]) is str
    assert type(response_data["id"]) is str
    assert type(response_data["submenus_count"]) is int
    assert type(response_data["dishes_count"]) is int
    assert response_data["title"] == title
    assert response_data["description"] == desc
    assert int(response_data["id"]) > 0
    assert response_data["submenus_count"] >= 0
    assert response_data["dishes_count"] >= 0

    # Update non-existant menu item
    response = client.patch(f'/api/v1/menus/0', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert type(response_data["detail"]) is str
    assert response_data["detail"] == "menu not found"

    # Delete menu item
    response = client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert type(response_data["status"]) is bool
    assert type(response_data["message"]) is str
    assert response_data["status"] == True
    assert response_data["message"] == "The menu has been deleted"

    # Delete non-existant menu item
    response = client.delete(f'/api/v1/menus/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert type(response_data["detail"]) is str
    assert response_data["detail"] == "menu not found"



"""____________________________SUBMENU_TESTS_____________________________"""

def test_crud_for_submenu():
    # Create menu
    menu_id = 0
    title = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(10))
    desc = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(10))
    response = client.post('/api/v1/menus', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data
    assert int(response_data["id"]) > 0
    menu_id = response_data["id"]

    # Create submenu
    submenu_id = 0
    response = client.post(f'/api/v1/menus/{menu_id}/submenus', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data
    assert type(response_data["title"]) is str
    assert type(response_data["description"]) is str
    assert type(response_data["id"]) is str
    assert type(response_data["dishes_count"]) is int
    assert response_data["title"] == title
    assert response_data["description"] == desc
    assert int(response_data["id"]) > 0
    assert response_data["dishes_count"] >= 0
    submenu_id = response_data["id"]

    # Get submenus list
    response = client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    for item in response_data:
        assert type(item["title"]) is str
        assert type(item["description"]) is str
        assert type(item["id"]) is str
        assert type(item["dishes_count"]) is int
        assert int(item["id"]) > 0
        assert item["dishes_count"] >= 0

    # Get submenu item
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert type(response_data["title"]) is str
    assert type(response_data["description"]) is str
    assert type(response_data["id"]) is str
    assert type(response_data["dishes_count"]) is int
    assert int(response_data["id"]) > 0
    assert response_data["dishes_count"] >= 0

    # Get non-existant submenu item
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert type(response_data["detail"]) is str
    assert response_data["detail"] == "submenu not found"

    # Update submenu item
    title += "1"
    desc += "1"
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert type(response_data["title"]) is str
    assert type(response_data["description"]) is str
    assert type(response_data["id"]) is str
    assert type(response_data["dishes_count"]) is int
    assert response_data["title"] == title
    assert response_data["description"] == desc
    assert int(response_data["id"]) > 0
    assert response_data["dishes_count"] >= 0

    # Update non-existant submenu item
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/0', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert type(response_data["detail"]) is str
    assert response_data["detail"] == "submenu not found"

    # Delete submenu item
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert type(response_data["status"]) is bool
    assert type(response_data["message"]) is str
    assert response_data["status"] == True
    assert response_data["message"] == "The submenu has been deleted"

    # Delete non-existant submenu item
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert type(response_data["detail"]) is str
    assert response_data["detail"] == "submenu not found"

    # Delete submenu item
    response = client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == status.HTTP_200_OK

"""____________________________DISH_TESTS_____________________________"""

def test_crud_for_dish():
    # Create menu
    menu_id = 0
    title = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(10))
    desc = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(10))
    response = client.post('/api/v1/menus', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data
    assert int(response_data["id"]) > 0
    menu_id = response_data["id"]

    # Create submenu
    submenu_id = 0
    response = client.post(f'/api/v1/menus/{menu_id}/submenus', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data
    assert int(response_data["id"]) > 0
    submenu_id = response_data["id"]

    # Create dish
    dish_id = 0
    response = client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data
    assert type(response_data["title"]) is str
    assert type(response_data["description"]) is str
    assert type(response_data["id"]) is str
    assert response_data["title"] == title
    assert response_data["description"] == desc
    assert int(response_data["id"]) > 0
    dish_id = response_data["id"]

    # Get dishes list
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    for item in response_data:
        assert type(item["title"]) is str
        assert type(item["description"]) is str
        assert type(item["id"]) is str
        assert int(item["id"]) > 0

    # Get dish item
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert type(response_data["title"]) is str
    assert type(response_data["description"]) is str
    assert type(response_data["id"]) is str
    assert int(response_data["id"]) > 0

    # Get non-existant dish item
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert type(response_data["detail"]) is str
    assert response_data["detail"] == "dish not found"

    # Update menu item
    title += "1"
    desc += "1"
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert type(response_data["title"]) is str
    assert type(response_data["description"]) is str
    assert type(response_data["id"]) is str
    assert response_data["title"] == title
    assert response_data["description"] == desc
    assert int(response_data["id"]) > 0

    # Update non-existant menu item
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/0', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert type(response_data["detail"]) is str
    assert response_data["detail"] == "dish not found"

    # Delete menu item
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert type(response_data["status"]) is bool
    assert type(response_data["message"]) is str
    assert response_data["status"] == True
    assert response_data["message"] == "The dish has been deleted"

    # Delete non-existant menu item
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert type(response_data["detail"]) is str
    assert response_data["detail"] == "dish not found"

    # Delete submenu item
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == status.HTTP_200_OK

    # Delete menu item
    response = client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == status.HTTP_200_OK
