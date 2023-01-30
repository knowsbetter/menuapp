from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

load_dotenv()

from . import cache, crud, models, schemes
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

cache.start()

# Dependency
def get_db():
    """Returns database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    path='/api/v1/menus/',
    response_model=schemes.Menu,
    summary='Создать меню',
    status_code=201
)
def create_menu(menu: schemes.MenuBase, db: Session = Depends(get_db)):
    """Create menu item"""
    db_menu = crud.MenuCRUD.get_menu_by_title(db=db, menu_title=menu.title)
    if db_menu:
        raise HTTPException(status_code=400, detail='menu already exists')
    return crud.MenuCRUD.create_menu(db=db, menu=menu)


@app.patch(
    path='/api/v1/menus/{menu_id}',
    summary='Обновить меню',
    response_model=schemes.Menu
)
def update_menu(menu_id: int, menu: schemes.MenuUpdate, db: Session = Depends(get_db)):
    """Update menu item"""
    db_menu = crud.MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)
    if db_menu:
        db_menu.title = menu.title
        db_menu.description = menu.description
        cache.set_cache(f'/api/v1/menus/{menu_id}', jsonable_encoder(db_menu))
        return crud.MenuCRUD.update_menu(db=db, menu_id=menu_id)
    else:
        raise HTTPException(status_code=404, detail='menu not found')


@app.get(
    path='/api/v1/menus/',
    summary='Просмотреть список меню',
    response_model=list[schemes.Menu]
)
def read_menus(db: Session = Depends(get_db)):
    """Read menus list"""
    menus = crud.MenuCRUD.get_menus(db=db)
    if menus:
        for menu in menus:
            cache.set_cache(f'/api/v1/menus/{menu.id}', jsonable_encoder(menu))
    return menus


@app.get(
    path='/api/v1/menus/{menu_id}',
    summary='Просмотреть конкретное меню',
    response_model=schemes.Menu
)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    """Read menu item"""
    cached = cache.get_cache(f'/api/v1/menus/{menu_id}')
    if cached:
        db_menu = cached
    else:
        db_menu = crud.MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    cache.set_cache(f'/api/v1/menus/{menu_id}', jsonable_encoder(db_menu))
    return db_menu


@app.delete(
    path='/api/v1/menus/{menu_id}',
    summary='Удалить меню',
    response_model=schemes.MenuDelete,
    status_code=200
)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """Delete menu item"""
    db_menu = crud.MenuCRUD.delete_menu(db=db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    cache.delete_cache(f'/api/v1/menus/{menu_id}')
    return {'status': True, 'message': 'The menu has been deleted'}


@app.post(
    path='/api/v1/menus/{menu_id}/submenus',
    summary='Создать подменю',
    response_model=schemes.Submenu,
    status_code=201
)
def create_submenu(menu_id: int, submenu: schemes.SubmenuBase, db: Session = Depends(get_db)):
    """Create submenu item"""
    db_submenu = crud.SubmenuCRUD.get_submenu_by_title(db=db, submenu_title=submenu.title)
    if db_submenu:
        raise HTTPException(status_code=400, detail='submenu already exists')
    cache.delete_cache(f'/api/v1/menus/{menu_id}')
    return crud.SubmenuCRUD.create_submenu(db=db, submenu=submenu, menu_id=menu_id)


@app.patch(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    summary='Обновить подменю',
    response_model=schemes.Submenu
)
def update_submenu(menu_id: int, submenu_id: int, submenu: schemes.SubmenuUpdate, db: Session = Depends(get_db)):
    """Update submenu item"""
    db_submenu = crud.SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if db_submenu:
        db_submenu.title = submenu.title
        db_submenu.description = submenu.description
        cache.set_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', jsonable_encoder(db_submenu))
        return crud.SubmenuCRUD.update_submenu(db=db, submenu_id=submenu_id)
    else:
        raise HTTPException(status_code=404, detail='submenu not found')


@app.get(
    path='/api/v1/menus/{menu_id}/submenus',
    summary='Просмотреть список подменю',
    response_model=list[schemes.Submenu]
)
def read_submenus(menu_id: int, db: Session = Depends(get_db)):
    """Read submenus list"""
    submenus = crud.SubmenuCRUD.get_submenus(db=db, menu_id=menu_id)
    if submenus:
        for submenu in submenus:
            cache.set_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu.id}', jsonable_encoder(submenu))
    return submenus


@app.get(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    summary='Просмотреть конкретное подменю',
    response_model=schemes.Submenu
)
def read_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """Read submenu item"""
    cached = cache.get_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    if cached:
        db_submenu = cached
    else:
        db_submenu = crud.SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    cache.set_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', jsonable_encoder(db_submenu))
    return db_submenu


@app.delete(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    summary='Удалить подменю',
    response_model=schemes.SubmenuDelete,
    status_code=200
)
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """Delete submenu item"""
    db_submenu = crud.SubmenuCRUD.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    cache.delete_cache(f'/api/v1/menus/{menu_id}')
    return {'status': True, 'message': 'The submenu has been deleted'}


@app.post(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    summary='Создать блюдо',
    response_model=schemes.Dish,
    status_code=201
)
def create_dish(menu_id: int, submenu_id: int, dish: schemes.DishBase, db: Session = Depends(get_db)):
    """Create dish item"""
    db_dish = crud.DishCRUD.get_dish_by_title(db=db, dish_title=dish.title)
    if db_dish:
        raise HTTPException(status_code=400, detail='dish already exists')
    cache.delete_cache(f'/api/v1/menus/{menu_id}')
    return crud.DishCRUD.create_dish(db=db, dish=dish, menu_id=menu_id, submenu_id=submenu_id)


@app.patch(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    summary='Обновить блюдо',
    response_model=schemes.Dish
)
def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: schemes.DishUpdate, db: Session = Depends(get_db)):
    """Update dish item"""
    db_dish = crud.DishCRUD.get_dish_by_id(db=db, dish_id=dish_id)
    if db_dish:
        db_dish.title = dish.title
        db_dish.description = dish.description
        db_dish.price = dish.price
        cache.set_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', jsonable_encoder(db_dish))
        return crud.DishCRUD.update_dish(db=db, dish_id=dish_id)
    else:
        raise HTTPException(status_code=404, detail='dish not found')


@app.get(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    summary='Просмотреть список блюд',
    response_model=list[schemes.Dish]
)
def read_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """Read dishes list"""
    dishes = crud.DishCRUD.get_dishes(db=db, submenu_id=submenu_id)
    if dishes:
        for dish in dishes:
            cache.set_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish.id}', jsonable_encoder(dish))
    return dishes


@app.get(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    summary='Просмотреть конкретное блюдо',
    response_model=schemes.Dish
)
def read_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    """Read dish item"""
    cached = cache.get_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    if cached:
        db_dish = cached
    else:
        db_dish = crud.DishCRUD.get_dish_by_id(db=db, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    cache.set_cache(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', jsonable_encoder(db_dish))
    return db_dish


@app.delete(
    path='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    summary='Удалить блюдо',
    response_model=schemes.DishDelete,
    status_code=200
)
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    """Delete dish item"""
    db_dish = crud.DishCRUD.delete_dish(db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    cache.delete_cache(f'/api/v1/menus/{menu_id}')
    return {'status': True, 'message': 'The dish has been deleted'}
