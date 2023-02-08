from fastapi import Depends, FastAPI, HTTPException

from services.cxl_service import CxlService
from services.cxl_service import get_cxl_service as cs
from services.dish_service import DishService
from services.dish_service import get_dish_service as ds
from services.menu_service import MenuService
from services.menu_service import get_menu_service as ms
from services.submenu_service import SubmenuService
from services.submenu_service import get_submenu_service as ss

from . import cache, crud, models, schemes
from .database import engine

app = FastAPI(title="Приложение для меню")


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.post(
    path="/api/v1/menus/",
    response_model=schemes.Menu,
    summary="Создать меню",
    status_code=201,
    tags=["Меню"],
)
async def create_menu(menu: schemes.MenuBase, menu_service: MenuService = Depends(ms)):
    """Create menu item"""
    res = await menu_service.create_menu(menu)
    if not res:
        raise HTTPException(status_code=400, detail="menu already exists")
    return res


@app.patch(
    path="/api/v1/menus/{menu_id}",
    summary="Обновить меню",
    response_model=schemes.Menu,
    tags=["Меню"],
)
async def update_menu(menu_id: int, menu: schemes.MenuUpdate, menu_service: MenuService = Depends(ms)):
    """Update menu item"""
    res = await menu_service.update_menu(menu_id, menu)
    if not res:
        raise HTTPException(status_code=404, detail="menu not found")
    return res


@app.get(
    path="/api/v1/menus/",
    summary="Просмотреть список меню",
    response_model=list[schemes.Menu],
    tags=["Меню"],
)
async def read_menus(menu_service: MenuService = Depends(ms)):
    """Read menus list"""
    return await menu_service.read_menus()


@app.get(
    path="/api/v1/menus/{menu_id}",
    summary="Просмотреть конкретное меню",
    response_model=schemes.Menu,
    tags=["Меню"],
)
async def read_menu(menu_id: int, menu_service: MenuService = Depends(ms)):
    """Read menu item"""
    res = await menu_service.read_menu(menu_id)
    if not res:
        raise HTTPException(status_code=404, detail="menu not found")
    return res


@app.delete(
    path="/api/v1/menus/{menu_id}",
    summary="Удалить меню",
    response_model=schemes.MenuDelete,
    status_code=200,
    tags=["Меню"],
)
async def delete_menu(menu_id: int, menu_service: MenuService = Depends(ms)):
    """Delete menu item"""
    res = await menu_service.delete_menu(menu_id)
    if not res:
        raise HTTPException(status_code=404, detail="menu not found")
    return res


@app.post(
    path="/api/v1/menus/{menu_id}/submenus",
    summary="Создать подменю",
    response_model=schemes.Submenu,
    status_code=201,
    tags=["Подменю"],
)
async def create_submenu(menu_id: int, submenu: schemes.SubmenuBase, submenu_service: SubmenuService = Depends(ss)):
    """Create submenu item"""
    res = await submenu_service.create_submenu(menu_id, submenu)
    if not res:
        raise HTTPException(status_code=400, detail="submenu already exists")
    return res


@app.patch(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    summary="Обновить подменю",
    response_model=schemes.Submenu,
    tags=["Подменю"],
)
async def update_submenu(
    menu_id: int, submenu_id: int, submenu: schemes.SubmenuUpdate, submenu_service: SubmenuService = Depends(ss)
):
    """Update submenu item"""
    res = await submenu_service.update_submenu(menu_id, submenu_id, submenu)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return res


@app.get(
    path="/api/v1/menus/{menu_id}/submenus",
    summary="Просмотреть список подменю",
    response_model=list[schemes.Submenu],
    tags=["Подменю"],
)
async def read_submenus(menu_id: int, submenu_service: SubmenuService = Depends(ss)):
    """Read submenus list"""
    return await submenu_service.read_submenus(menu_id)


@app.get(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    summary="Просмотреть конкретное подменю",
    response_model=schemes.Submenu,
    tags=["Подменю"],
)
async def read_submenu(menu_id: int, submenu_id: int, submenu_service: SubmenuService = Depends(ss)):
    """Read submenu item"""
    res = await submenu_service.read_submenu(menu_id, submenu_id)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return res


@app.delete(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    summary="Удалить подменю",
    response_model=schemes.SubmenuDelete,
    status_code=200,
    tags=["Подменю"],
)
async def delete_submenu(menu_id: int, submenu_id: int, submenu_service: SubmenuService = Depends(ss)):
    """Delete submenu item"""
    res = await submenu_service.delete_submenu(menu_id, submenu_id)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return res


@app.post(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    summary="Создать блюдо",
    response_model=schemes.Dish,
    status_code=201,
    tags=["Блюда"],
)
async def create_dish(
    menu_id: int,
    submenu_id: int,
    dish: schemes.DishBase,
    dish_service: DishService = Depends(ds),
):
    """Create dish item"""
    res = await dish_service.create_dish(menu_id, submenu_id, dish)
    if not res:
        raise HTTPException(status_code=400, detail="dish already exists")
    return res


@app.patch(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Обновить блюдо",
    response_model=schemes.Dish,
    tags=["Блюда"],
)
async def update_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish: schemes.DishUpdate,
    dish_service: DishService = Depends(ds),
):
    """Update dish item"""
    res = await dish_service.update_dish(menu_id, submenu_id, dish_id, dish)
    if not res:
        raise HTTPException(status_code=404, detail="dish not found")
    return res


@app.get(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    summary="Просмотреть список блюд",
    response_model=list[schemes.Dish],
    tags=["Блюда"],
)
async def read_dishes(
    menu_id: int,
    submenu_id: int,
    dish_service: DishService = Depends(ds),
):
    """Read dishes list"""
    return await dish_service.read_dishes(menu_id, submenu_id)


@app.get(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Просмотреть конкретное блюдо",
    response_model=schemes.Dish,
    tags=["Блюда"],
)
async def read_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish_service: DishService = Depends(ds),
):
    """Read dish item"""
    res = await dish_service.read_dish(menu_id, submenu_id, dish_id)
    if not res:
        raise HTTPException(status_code=404, detail="dish not found")
    return res


@app.delete(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Удалить блюдо",
    response_model=schemes.DishDelete,
    status_code=200,
    tags=["Блюда"],
)
async def delete_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish_service: DishService = Depends(ds),
):
    """Delete dish item"""
    res = await dish_service.delete_dish(menu_id, submenu_id, dish_id)
    if not res:
        raise HTTPException(status_code=404, detail="dish not found")
    return res


@app.post(
    path="/api/v1/fill/",
    summary="1. Создание тестового меню",
    status_code=201,
    tags=["Выгрузка тестового меню в excel-файл"],
)
async def create_test_menu(password: schemes.Password, cxl_service: CxlService = Depends(cs)):
    """Create test menu"""
    res = await cxl_service.create_test_menu(password)
    if not res:
        return {"status": False, "message": "Incorrect password"}
    return res


@app.post(
    path="/api/v1/xl/create/",
    summary="2. Запрос на генерацию эксель файла",
    status_code=200,
    tags=["Выгрузка тестового меню в excel-файл"],
)
async def create_excel_file(cxl_service: CxlService = Depends(cs)):
    """Create test menu"""
    return await cxl_service.create_excel_file()


@app.get(
    path="/api/v1/xl/get/",
    summary="3. Получение ссылки на скачивание файла или уточнение статуса обработки",
    tags=["Выгрузка тестового меню в excel-файл"],
)
async def download_xl(task_id: str):
    if cache.get_cache(f"celery{task_id}"):
        return await crud.CreateXL.get_xl(task_id)
    else:
        return {"status": False, "message": "Please request to generate excel file first"}
