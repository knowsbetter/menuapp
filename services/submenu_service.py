from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from menuapp import cache, crud, schemes
from menuapp.database import SessionLocal


async def get_db():
    """Returns database session"""
    async with SessionLocal() as db:
        yield db


class SubmenuService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_submenu(self, menu_id: int, submenu: schemes.SubmenuBase):
        db_submenu = await crud.SubmenuCRUD.get_submenu_by_title(submenu_title=submenu.title, db=self.session)
        if db_submenu:
            return None
        await cache.delete_cache(f"/api/v1/menus/{menu_id}")
        return await crud.SubmenuCRUD.create_submenu(db=self.session, submenu=submenu, menu_id=menu_id)

    async def update_submenu(self, menu_id: int, submenu_id: int, submenu: schemes.SubmenuUpdate):
        db_submenu = await crud.SubmenuCRUD.get_submenu_by_id(db=self.session, submenu_id=submenu_id)
        if db_submenu:
            db_submenu.title = submenu.title
            db_submenu.description = submenu.description
            await cache.set_cache(
                f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
                jsonable_encoder(db_submenu),
            )
            return await crud.SubmenuCRUD.update_submenu(db=self.session, submenu_id=submenu_id)
        else:
            return None

    async def read_submenus(self, menu_id: int):
        submenus = await crud.SubmenuCRUD.get_submenus(db=self.session, menu_id=menu_id)
        if submenus:
            for submenu in submenus:
                await cache.set_cache(
                    f"/api/v1/menus/{menu_id}/submenus/{submenu.id}",
                    jsonable_encoder(submenu),
                )
        return submenus

    async def read_submenu(self, menu_id: int, submenu_id: int):
        cached = await cache.get_cache(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
        if cached:
            db_submenu = cached
        else:
            db_submenu = await crud.SubmenuCRUD.get_submenu_by_id(db=self.session, submenu_id=submenu_id)
        if db_submenu is None:
            return None
        await cache.set_cache(
            f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
            jsonable_encoder(db_submenu),
        )
        return db_submenu

    async def delete_submenu(self, menu_id: int, submenu_id: int):
        db_submenu = await crud.SubmenuCRUD.delete_submenu(db=self.session, menu_id=menu_id, submenu_id=submenu_id)
        if db_submenu is None:
            return None
        await cache.delete_cache(f"/api/v1/menus/{menu_id}")
        return {"status": True, "message": "The submenu has been deleted"}


def get_submenu_service(session: AsyncSession = Depends(get_db)):
    return SubmenuService(session)
