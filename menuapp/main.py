from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from . import cache, config, crud, models, schemes
from .database import SessionLocal, engine

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


# Dependency
async def get_db():
    """Returns database session"""
    async with SessionLocal() as db:
        yield db


@app.on_event("shutdown")
async def shutdown_event():
    await cache.stop()
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


@app.post(
    path="/api/v1/menus/",
    response_model=schemes.Menu,
    summary="Создать меню",
    status_code=201,
)
async def create_menu(menu: schemes.MenuBase, db: AsyncSession = Depends(get_db)):
    """Create menu item"""
    db_menu = await crud.MenuCRUD.get_menu_by_title(db=db, menu_title=menu.title)
    if db_menu:
        raise HTTPException(status_code=400, detail="menu already exists")
    return await crud.MenuCRUD.create_menu(db=db, menu=menu)


@app.patch(
    path="/api/v1/menus/{menu_id}",
    summary="Обновить меню",
    response_model=schemes.Menu,
)
async def update_menu(menu_id: int, menu: schemes.MenuUpdate, db: AsyncSession = Depends(get_db)):
    """Update menu item"""
    db_menu = await crud.MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)
    if db_menu:
        db_menu.title = menu.title
        db_menu.description = menu.description
        await cache.set_cache(f"/api/v1/menus/{menu_id}", jsonable_encoder(db_menu))
        return await crud.MenuCRUD.update_menu(db=db, menu_id=menu_id)
    else:
        raise HTTPException(status_code=404, detail="menu not found")


@app.get(
    path="/api/v1/menus/",
    summary="Просмотреть список меню",
    response_model=list[schemes.Menu],
)
async def read_menus(db: AsyncSession = Depends(get_db)):
    """Read menus list"""
    menus = await crud.MenuCRUD.get_menus(db=db)
    if menus:
        for menu in menus:
            await cache.set_cache(f"/api/v1/menus/{menu.id}", jsonable_encoder(menu))
    return menus


@app.get(
    path="/api/v1/menus/{menu_id}",
    summary="Просмотреть конкретное меню",
    response_model=schemes.Menu,
)
async def read_menu(menu_id: int, db: AsyncSession = Depends(get_db)):
    """Read menu item"""
    cached = await cache.get_cache(f"/api/v1/menus/{menu_id}")
    if cached:
        db_menu = cached
    else:
        db_menu = await crud.MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    await cache.set_cache(f"/api/v1/menus/{menu_id}", jsonable_encoder(db_menu))
    return db_menu


@app.delete(
    path="/api/v1/menus/{menu_id}",
    summary="Удалить меню",
    response_model=schemes.MenuDelete,
    status_code=200,
)
async def delete_menu(menu_id: int, db: AsyncSession = Depends(get_db)):
    """Delete menu item"""
    db_menu = await crud.MenuCRUD.delete_menu(db=db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    await cache.delete_cache(f"/api/v1/menus/{menu_id}")
    return {"status": True, "message": "The menu has been deleted"}


@app.post(
    path="/api/v1/menus/{menu_id}/submenus",
    summary="Создать подменю",
    response_model=schemes.Submenu,
    status_code=201,
)
async def create_submenu(menu_id: int, submenu: schemes.SubmenuBase, db: AsyncSession = Depends(get_db)):
    """Create submenu item"""
    db_submenu = await crud.SubmenuCRUD.get_submenu_by_title(db=db, submenu_title=submenu.title)
    if db_submenu:
        raise HTTPException(status_code=400, detail="submenu already exists")
    await cache.delete_cache(f"/api/v1/menus/{menu_id}")
    return await crud.SubmenuCRUD.create_submenu(db=db, submenu=submenu, menu_id=menu_id)


@app.patch(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    summary="Обновить подменю",
    response_model=schemes.Submenu,
)
async def update_submenu(
    menu_id: int,
    submenu_id: int,
    submenu: schemes.SubmenuUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update submenu item"""
    db_submenu = await crud.SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if db_submenu:
        db_submenu.title = submenu.title
        db_submenu.description = submenu.description
        await cache.set_cache(
            f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
            jsonable_encoder(db_submenu),
        )
        return await crud.SubmenuCRUD.update_submenu(db=db, submenu_id=submenu_id)
    else:
        raise HTTPException(status_code=404, detail="submenu not found")


@app.get(
    path="/api/v1/menus/{menu_id}/submenus",
    summary="Просмотреть список подменю",
    response_model=list[schemes.Submenu],
)
async def read_submenus(menu_id: int, db: AsyncSession = Depends(get_db)):
    """Read submenus list"""
    submenus = await crud.SubmenuCRUD.get_submenus(db=db, menu_id=menu_id)
    if submenus:
        for submenu in submenus:
            await cache.set_cache(
                f"/api/v1/menus/{menu_id}/submenus/{submenu.id}",
                jsonable_encoder(submenu),
            )
    return submenus


@app.get(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    summary="Просмотреть конкретное подменю",
    response_model=schemes.Submenu,
)
async def read_submenu(menu_id: int, submenu_id: int, db: AsyncSession = Depends(get_db)):
    """Read submenu item"""
    cached = await cache.get_cache(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    if cached:
        db_submenu = cached
    else:
        db_submenu = await crud.SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    await cache.set_cache(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
        jsonable_encoder(db_submenu),
    )
    return db_submenu


@app.delete(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    summary="Удалить подменю",
    response_model=schemes.SubmenuDelete,
    status_code=200,
)
async def delete_submenu(menu_id: int, submenu_id: int, db: AsyncSession = Depends(get_db)):
    """Delete submenu item"""
    db_submenu = await crud.SubmenuCRUD.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    await cache.delete_cache(f"/api/v1/menus/{menu_id}")
    return {"status": True, "message": "The submenu has been deleted"}


@app.post(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    summary="Создать блюдо",
    response_model=schemes.Dish,
    status_code=201,
)
async def create_dish(
    menu_id: int,
    submenu_id: int,
    dish: schemes.DishBase,
    db: AsyncSession = Depends(get_db),
):
    """Create dish item"""
    db_dish = await crud.DishCRUD.get_dish_by_title(db=db, dish_title=dish.title)
    if db_dish:
        raise HTTPException(status_code=400, detail="dish already exists")
    await cache.delete_cache(f"/api/v1/menus/{menu_id}")
    return await crud.DishCRUD.create_dish(db=db, dish=dish, menu_id=menu_id, submenu_id=submenu_id)


@app.patch(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Обновить блюдо",
    response_model=schemes.Dish,
)
async def update_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish: schemes.DishUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update dish item"""
    db_dish = await crud.DishCRUD.get_dish_by_id(db=db, dish_id=dish_id)
    if db_dish:
        db_dish.title = dish.title
        db_dish.description = dish.description
        db_dish.price = dish.price
        await cache.set_cache(
            f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
            jsonable_encoder(db_dish),
        )
        return await crud.DishCRUD.update_dish(db=db, dish_id=dish_id)
    else:
        raise HTTPException(status_code=404, detail="dish not found")


@app.get(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    summary="Просмотреть список блюд",
    response_model=list[schemes.Dish],
)
async def read_dishes(menu_id: int, submenu_id: int, db: AsyncSession = Depends(get_db)):
    """Read dishes list"""
    dishes = await crud.DishCRUD.get_dishes(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if dishes:
        for dish in dishes:
            await cache.set_cache(
                f"/api/v1/menus/{menu_id}/submenus/\
                    {submenu_id}/dishes/{dish.id}",
                jsonable_encoder(dish),
            )
    return dishes


@app.get(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Просмотреть конкретное блюдо",
    response_model=schemes.Dish,
)
async def read_dish(menu_id: int, submenu_id: int, dish_id: int, db: AsyncSession = Depends(get_db)):
    """Read dish item"""
    cached = await cache.get_cache(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    if cached:
        db_dish = cached
    else:
        db_dish = await crud.DishCRUD.get_dish_by_id(db=db, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    await cache.set_cache(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        jsonable_encoder(db_dish),
    )
    return db_dish


@app.delete(
    path="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    summary="Удалить блюдо",
    response_model=schemes.DishDelete,
    status_code=200,
)
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: AsyncSession = Depends(get_db)):
    """Delete dish item"""
    db_dish = await crud.DishCRUD.delete_dish(db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    await cache.delete_cache(f"/api/v1/menus/{menu_id}")
    return {"status": True, "message": "The dish has been deleted"}


@app.post(
    path="/api/v1/fill/",
    summary="Создать тестовое меню",
    status_code=201,
)
async def create_test_menu(password: schemes.Password, db: AsyncSession = Depends(get_db)):
    """Create test menu"""
    if password.password == config.SPECIAL_PASSWORD:
        await crud.FillMenu.fill(db)
        return {"status": True, "message": "Success"}
    else:
        return {"status": False, "message": "Incorrect password"}


@app.post(path="/api/v1/xl/create/", summary="Запрос на генерацию эксель файла", status_code=200)
async def create_excel_file(password: schemes.Password, db: AsyncSession = Depends(get_db)):
    """Create test menu"""
    if password.password == config.SPECIAL_PASSWORD:
        res = await crud.CreateXL.create_xl(db)
        return {"status": True, "message": f"{res}"}
    else:
        return {"status": False, "message": "Incorrect password"}


@app.get(
    path="/api/v1/xl/get/",
    summary="Скачать файл или получить статус",
)
async def download_xl():
    return await crud.CreateXL.get_xl()
