from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from menuapp import cache, crud, schemes
from menuapp.database import SessionLocal


async def get_db():
    """Returns database session"""
    async with SessionLocal() as db:
        yield db


class MenuService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_menu(self, menu: schemes.MenuBase):
        db_menu = await crud.MenuCRUD.get_menu_by_title(menu_title=menu.title, db=self.session)
        if db_menu:
            return None
        return await crud.MenuCRUD.create_menu(menu=menu, db=self.session)

    async def update_menu(self, menu_id: int, menu: schemes.MenuUpdate):
        db_menu = await crud.MenuCRUD.get_menu_by_id(menu_id=menu_id, db=self.session)
        if db_menu:
            db_menu.title = menu.title
            db_menu.description = menu.description
            await cache.set_cache(f"/api/v1/menus/{menu_id}", jsonable_encoder(db_menu))
            return await crud.MenuCRUD.update_menu(menu_id=menu_id, db=self.session)
        else:
            return None

    async def read_menus(self):
        menus = await crud.MenuCRUD.get_menus(db=self.session)
        if menus:
            for menu in menus:
                await cache.set_cache(f"/api/v1/menus/{menu.id}", jsonable_encoder(menu))
        return menus

    async def read_menu(self, menu_id: int):
        cached = await cache.get_cache(f"/api/v1/menus/{menu_id}")
        if cached:
            db_menu = cached
        else:
            db_menu = await crud.MenuCRUD.get_menu_by_id(menu_id=menu_id, db=self.session)
        if db_menu is None:
            return None
        await cache.set_cache(f"/api/v1/menus/{menu_id}", jsonable_encoder(db_menu))
        return db_menu

    async def delete_menu(self, menu_id: int):
        db_menu = await crud.MenuCRUD.delete_menu(menu_id=menu_id, db=self.session)
        if db_menu is None:
            return None
        await cache.delete_cache(f"/api/v1/menus/{menu_id}")
        return {"status": True, "message": "The menu has been deleted"}


def get_menu_service(session: AsyncSession = Depends(get_db)):
    return MenuService(session)
