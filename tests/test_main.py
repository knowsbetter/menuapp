from fastapi.testclient import TestClient
from fastapi import status
from menuapp.main import app
import random
from datetime import datetime

random.seed(datetime.now().timestamp())

client = TestClient(app=app)

menu_id = 0
submenu_id = 0
dish_id = 0

title = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(10))
desc = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(10))

"""____________________________MENU_TESTS_____________________________"""

def test_create_menu_item():
    global menu_id
    response = client.post('/api/v1/menus', json={"title": title, "description": desc})
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED]
    response_data = response.json()
    assert response_data
    if response.status_code == status.HTTP_201_CREATED:
        assert response_data["title"] == title
        assert response_data["description"] == desc
        assert int(response_data["id"]) > 0
        assert response_data["submenus_count"] >= 0
        assert response_data["dishes_count"] >= 0
        menu_id = response_data["id"]
    else:
        assert response_data["detail"] == "menu already exists"

def test_get_menus_list():
    response = client.get('/api/v1/menus')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    for item in response_data:
        assert type(item["title"]) is str
        assert type(item["description"]) is str
        assert int(item["id"]) > 0
        assert item["submenus_count"] >= 0
        assert item["dishes_count"] >= 0

def test_get_menu_item():
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    response_data = response.json()
    assert response_data
    if response.status_code == status.HTTP_200_OK:
        assert response_data["title"] == title
        assert response_data["description"] == desc
        assert int(response_data["id"]) > 0
        assert response_data["submenus_count"] >= 0
        assert response_data["dishes_count"] >= 0
    else:
        assert response_data["detail"] == "menu not found"

def test_get_nonexistant_menu_item():
    response = client.get('/api/v1/menus/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert response_data["detail"] == "menu not found"

def test_update_menu_item():
    response = client.patch(f'/api/v1/menus/{menu_id}', json={"title": title + "1", "description": desc + "1"})
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["title"] == title + "1"
    assert response_data["description"] == desc + "1"
    assert int(response_data["id"]) > 0
    assert response_data["submenus_count"] >= 0
    assert response_data["dishes_count"] >= 0

def test_update_nonexistant_menu_item():
    response = client.patch(f'/api/v1/menus/0', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert response_data["detail"] == "menu not found"

def test_delete_menu_item():
    response = client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert response_data["status"] == True
    assert response_data["message"] == "The menu has been deleted"

def test_delete_nonexistant_menu_item():
    response = client.delete(f'/api/v1/menus/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert response_data["detail"] == "menu not found"

"""____________________________SUBMENU_TESTS_____________________________"""

def test_create_submenu_item():
    global menu_id, submenu_id
    test_create_menu_item()
    response = client.post(f'/api/v1/menus/{menu_id}/submenus', json={"title": title, "description": desc})
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED]
    response_data = response.json()
    assert response_data
    if response.status_code == status.HTTP_201_CREATED:
        assert response_data["title"] == title
        assert response_data["description"] == desc
        assert int(response_data["id"]) > 0
        assert response_data["dishes_count"] >= 0
        submenu_id = response_data["id"]
    else:
        assert response_data["detail"] == "submenu already exists"

def test_get_submenus_list():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    for item in response_data:
        assert type(item["title"]) is str
        assert type(item["description"]) is str
        assert int(item["id"]) > 0
        assert item["dishes_count"] >= 0

def test_get_submenu_item():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    response_data = response.json()
    assert response_data
    if response.status_code == status.HTTP_200_OK:
        assert response_data["title"] == title
        assert response_data["description"] == desc
        assert int(response_data["id"]) > 0
        assert response_data["dishes_count"] >= 0
    else:
        assert response_data["detail"] == "submenu not found"

def test_get_nonexistant_submenu_item():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert response_data["detail"] == "submenu not found"

def test_update_submenu_item():
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json={"title": title + "1", "description": desc + "1"})
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert response_data["title"] == title + "1"
    assert response_data["description"] == desc + "1"
    assert int(response_data["id"]) > 0
    assert response_data["dishes_count"] >= 0

def test_update_nonexistant_submenu_item():
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/0', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert response_data["detail"] == "submenu not found"

def test_delete_submenu_item():
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert response_data["status"] == True
    assert response_data["message"] == "The submenu has been deleted"

def test_delete_nonexistant_submenu_item():
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert response_data["detail"] == "submenu not found"
    test_delete_menu_item()

"""____________________________DISH_TESTS_____________________________"""

def test_create_dish_item():
    global menu_id, submenu_id, dish_id
    test_create_submenu_item()
    response = client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json={"title": title, "description": desc})
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED]
    response_data = response.json()
    assert response_data
    if response.status_code == status.HTTP_201_CREATED:
        assert response_data["title"] == title
        assert response_data["description"] == desc
        assert int(response_data["id"]) > 0
        dish_id = response_data["id"]
    elif response.status_code == status.HTTP_400_BAD_REQUEST:
        assert response_data["detail"] == "dish already exists"
    

def test_get_dishes_list():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    for item in response_data:
        assert type(item["title"]) is str
        assert type(item["description"]) is str
        assert int(item["id"]) > 0

def test_get_dish_item():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    response_data = response.json()
    assert response_data
    if response.status_code == status.HTTP_200_OK:
        assert response_data["title"] == title
        assert response_data["description"] == desc
        assert int(response_data["id"]) > 0
    else:
        assert response_data["detail"] == "dish not found"

def test_get_nonexistant_dich_item():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert response_data["detail"] == "dish not found"

def test_update_dish_item():
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json={"title": title + "1", "description": desc + "1"})
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert response_data["title"] == title + "1"
    assert response_data["description"] == desc + "1"
    assert int(response_data["id"]) > 0

def test_update_nonexistant_dich_item():
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/0', json={"title": title, "description": desc})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert response_data["detail"] == "dish not found"

def test_delete_dish_item():
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data
    assert response_data["status"] == True
    assert response_data["message"] == "The dish has been deleted"

def test_nonexistant_dich_item():
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data
    assert response_data["detail"] == "dish not found"
    test_delete_submenu_item()