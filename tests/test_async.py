import random
from datetime import datetime

import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import status

from menuapp.main import app

random.seed(datetime.now().timestamp())

menu_id = 0
submenu_id = 0
dish_id = 0

title = "".join(random.choice("abcasync defghijklmnopqrstuvwxyz") for i in range(10))
desc = "".join(random.choice("abcasync defghijklmnopqrstuvwxyz") for i in range(10))


@pytest.mark.asyncio
class TestMenu:
    async def test_create_menu_item(self):
        """Tests menu item creation"""
        global menu_id
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/v1/menus/", json={"title": title, "description": desc})
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_201_CREATED,
        ]
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

    async def test_get_menus_list(self):
        """Tests menus list getter"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/api/v1/menus/")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data
        for item in response_data:
            assert type(item["title"]) is str
            assert type(item["description"]) is str
            assert int(item["id"]) > 0
            assert item["submenus_count"] >= 0
            assert item["dishes_count"] >= 0

    @pytest.mark.asyncio
    async def test_get_menu_item(self):
        """Tests menu item getter"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(f"/api/v1/menus/{menu_id}")
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND,
        ]
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

    @pytest.mark.asyncio
    async def test_get_nonexistant_menu_item(self):
        """Tests no menu getter"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/api/v1/menus/0")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert response_data
        assert response_data["detail"] == "menu not found"

    @pytest.mark.asyncio
    async def test_update_menu_item(self):
        """Tests menu item update"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.patch(
                    f"/api/v1/menus/{menu_id}",
                    json={"title": title + "1", "description": desc + "1"},
                )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["title"] == title + "1"
        assert response_data["description"] == desc + "1"
        assert int(response_data["id"]) > 0
        assert response_data["submenus_count"] >= 0
        assert response_data["dishes_count"] >= 0

    @pytest.mark.asyncio
    async def test_update_nonexistant_menu_item(self):
        """Tests no menu item update"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.patch("/api/v1/menus/0", json={"title": title, "description": desc})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert response_data
        assert response_data["detail"] == "menu not found"

    @pytest.mark.asyncio
    async def test_delete_menu_item(self):
        """Tests menu item removal"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.delete(f"/api/v1/menus/{menu_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data
        assert response_data["status"] is True
        assert response_data["message"] == "The menu has been deleted"

    @pytest.mark.asyncio
    async def test_delete_nonexistant_menu_item(self):
        """Tests no menu item removal"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.delete("/api/v1/menus/0")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert response_data
        assert response_data["detail"] == "menu not found"


class TestSubmenu:
    @pytest.mark.asyncio
    async def test_create_submenu_item(self):
        """Tests submenu item creation"""
        global menu_id, submenu_id
        await TestMenu.test_create_menu_item(TestSubmenu())
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/v1/menus/{menu_id}/submenus",
                json={"title": title, "description": desc},
            )
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_201_CREATED,
        ]
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

    @pytest.mark.asyncio
    async def test_get_submenus_list(self):
        """Tests submenus list getter"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(f"/api/v1/menus/{menu_id}/submenus")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data
        for item in response_data:
            assert type(item["title"]) is str
            assert type(item["description"]) is str
            assert int(item["id"]) > 0
            assert item["dishes_count"] >= 0

    @pytest.mark.asyncio
    async def test_get_submenu_item(self):
        """Tests submenu item getter"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND,
        ]
        response_data = response.json()
        assert response_data
        if response.status_code == status.HTTP_200_OK:
            assert response_data["title"] == title
            assert response_data["description"] == desc
            assert int(response_data["id"]) > 0
            assert response_data["dishes_count"] >= 0
        else:
            assert response_data["detail"] == "submenu not found"

    @pytest.mark.asyncio
    async def test_get_nonexistant_submenu_item(self):
        """Tests no submenu item getter"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(f"/api/v1/menus/{menu_id}/submenus/0")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert response_data
        assert response_data["detail"] == "submenu not found"

    @pytest.mark.asyncio
    async def test_update_submenu_item(self):
        """Tests submenu item update"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.patch(
                    f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
                    json={"title": title + "1", "description": desc + "1"},
                )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data
        assert response_data["title"] == title + "1"
        assert response_data["description"] == desc + "1"
        assert int(response_data["id"]) > 0
        assert response_data["dishes_count"] >= 0

    @pytest.mark.asyncio
    async def test_update_nonexistant_submenu_item(self):
        """Tests no submenu item update"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.patch(
                    f"/api/v1/menus/{menu_id}/submenus/0",
                    json={"title": title, "description": desc},
                )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert response_data
        assert response_data["detail"] == "submenu not found"

    @pytest.mark.asyncio
    async def test_delete_submenu_item(self):
        """Tests submenu item removal"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data
        assert response_data["status"] is True
        assert response_data["message"] == "The submenu has been deleted"

    @pytest.mark.asyncio
    async def test_delete_nonexistant_submenu_item(self):
        """Tests nosubmenu item removal"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.delete(f"/api/v1/menus/{menu_id}/submenus/0")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert response_data
        assert response_data["detail"] == "submenu not found"
        TestMenu.test_delete_menu_item(TestMenu())


class TestDish:
    @pytest.mark.asyncio
    async def test_create_dish_item(self):
        """Tests dish item creation"""
        global menu_id, submenu_id, dish_id
        await TestSubmenu.test_create_submenu_item(TestSubmenu())
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
                json={"title": title, "description": desc},
            )
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_201_CREATED,
        ]
        response_data = response.json()
        assert response_data
        if response.status_code == status.HTTP_201_CREATED:
            assert response_data["title"] == title
            assert response_data["description"] == desc
            assert int(response_data["id"]) > 0
            dish_id = response_data["id"]
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            assert response_data["detail"] == "dish already exists"

    @pytest.mark.asyncio
    async def test_get_dishes_list(self):
        """Tests dishes list getter"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data
        for item in response_data:
            assert type(item["title"]) is str
            assert type(item["description"]) is str
            assert int(item["id"]) > 0

    @pytest.mark.asyncio
    async def test_get_dish_item(self):
        """Tests dish item getter"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND,
        ]
        response_data = response.json()
        assert response_data
        if response.status_code == status.HTTP_200_OK:
            assert response_data["title"] == title
            assert response_data["description"] == desc
            assert int(response_data["id"]) > 0
        else:
            assert response_data["detail"] == "dish not found"

    @pytest.mark.asyncio
    async def test_get_nonexistant_dich_item(self):
        """Tests no dish item getter"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/0")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert response_data
        assert response_data["detail"] == "dish not found"

    @pytest.mark.asyncio
    async def test_update_dish_item(self):
        """Tests dish item update"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.patch(
                    f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                    json={"title": title + "1", "description": desc + "1"},
                )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data
        assert response_data["title"] == title + "1"
        assert response_data["description"] == desc + "1"
        assert int(response_data["id"]) > 0

    @pytest.mark.asyncio
    async def test_update_nonexistant_dich_item(self):
        """Tests no dish item update"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.patch(
                    f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/0",
                    json={"title": title, "description": desc},
                )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert response_data
        assert response_data["detail"] == "dish not found"

    @pytest.mark.asyncio
    async def test_delete_dish_item(self):
        """Tests dish item removal"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data
        assert response_data["status"] is True
        assert response_data["message"] == "The dish has been deleted"

    @pytest.mark.asyncio
    async def test_nonexistant_dish_item(self):
        """Tests no dish item removal"""
        async with LifespanManager(app):
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/0")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert response_data
        assert response_data["detail"] == "dish not found"
        TestSubmenu.test_delete_submenu_item(TestSubmenu())
