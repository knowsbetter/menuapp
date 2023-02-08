from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from menuapp import cache, crud, schemes
from menuapp.database import SessionLocal


async def get_db():
    """Returns database session"""
    async with SessionLocal() as db:
        yield db


class DishService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_dish(self, menu_id: int, submenu_id: int, dish: schemes.DishBase):
        db_dish = await crud.DishCRUD.get_dish_by_title(db=self.session, dish_title=dish.title)
        if db_dish:
            return None
        await cache.delete_cache(f"/api/v1/menus/{menu_id}")
        return await crud.DishCRUD.create_dish(db=self.session, dish=dish, menu_id=menu_id, submenu_id=submenu_id)

    async def update_dish(self, menu_id: int, submenu_id: int, dish_id: int, dish: schemes.DishUpdate):
        db_dish = await crud.DishCRUD.get_dish_by_id(db=self.session, dish_id=dish_id)
        if db_dish:
            db_dish.title = dish.title
            db_dish.description = dish.description
            db_dish.price = dish.price
            await cache.set_cache(
                f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                jsonable_encoder(db_dish),
            )
            return await crud.DishCRUD.update_dish(db=self.session, dish_id=dish_id)
        else:
            return None

    async def read_dishes(self, menu_id: int, submenu_id: int):
        dishes = await crud.DishCRUD.get_dishes(db=self.session, menu_id=menu_id, submenu_id=submenu_id)
        if dishes:
            for dish in dishes:
                await cache.set_cache(
                    f"/api/v1/menus/{menu_id}/submenus/\
                    {submenu_id}/dishes/{dish.id}",
                    jsonable_encoder(dish),
                )
        return dishes

    async def read_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        cached = await cache.get_cache(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
        if cached:
            db_dish = cached
        else:
            db_dish = await crud.DishCRUD.get_dish_by_id(db=self.session, dish_id=dish_id)
        if db_dish is None:
            return None
        await cache.set_cache(
            f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
            jsonable_encoder(db_dish),
        )
        return db_dish

    async def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        db_dish = await crud.DishCRUD.delete_dish(
            db=self.session, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id
        )
        if db_dish is None:
            return None
        await cache.delete_cache(f"/api/v1/menus/{menu_id}")
        return {"status": True, "message": "The dish has been deleted"}


def get_dish_service(session: AsyncSession = Depends(get_db)):
    return DishService(session)
