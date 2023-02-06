import json

import aiofiles
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from transport.tasks import to_excel

from . import models, schemes


class MenuCRUD:
    @staticmethod
    async def get_menu_by_id(db: AsyncSession, menu_id: int):
        """Get menu by id"""
        return (await db.execute(select(models.Menu).where(models.Menu.id == menu_id))).scalar()

    @staticmethod
    async def get_menu_by_title(db: AsyncSession, menu_title: str):
        "Get menu by title"
        return (await db.execute(select(models.Menu).where(models.Menu.title == menu_title))).scalar()

    @staticmethod
    async def get_menus(db: AsyncSession):
        """Get menus list"""
        return (await db.execute(select(models.Menu))).scalars().all()

    @staticmethod
    async def create_menu(db: AsyncSession, menu: schemes.MenuBase):
        """Create menu item"""
        db_menu = models.Menu(**menu.dict())
        db_menu.dishes_count = 0
        db_menu.submenus_count = 0
        db.add(db_menu)
        await db.commit()
        return db_menu

    @staticmethod
    async def delete_menu(db: AsyncSession, menu_id: int):
        """Delete menu item"""
        db_menu = await MenuCRUD.get_menu_by_id(db, menu_id)
        if db_menu is None:
            return None
        else:
            await db.delete(db_menu)
            await db.commit()
            return True

    @staticmethod
    async def update_menu(db: AsyncSession, menu_id: int):
        """Update menu item"""
        await db.commit()
        return await MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)


class SubmenuCRUD:
    @staticmethod
    async def get_submenu_by_id(db: AsyncSession, submenu_id: int):
        """Get submenu by id"""
        return (await db.execute(select(models.Submenu).where(models.Submenu.id == submenu_id))).scalar()

    @staticmethod
    async def get_submenu_by_title(db: AsyncSession, submenu_title: str):
        """Get submenu by title"""
        return (await db.execute(select(models.Submenu).where(models.Submenu.title == submenu_title))).scalar()

    @staticmethod
    async def get_submenus(menu_id: int, db: AsyncSession):
        """Get submenus list"""
        return (await db.execute(select(models.Submenu).where(models.Submenu.menu_id == menu_id))).scalars().all()

    @staticmethod
    async def create_submenu(db: AsyncSession, submenu: schemes.SubmenuBase, menu_id: int):
        """Create submenu item"""
        db_submenu = models.Submenu(**submenu.dict())
        db_submenu.menu_id = menu_id
        db_submenu.dishes_count = 0
        (await MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)).submenus_count += 1
        db.add(db_submenu)
        await db.commit()
        return db_submenu

    @staticmethod
    async def delete_submenu(db: AsyncSession, menu_id: int, submenu_id: int):
        """Delete submenu item"""
        db_submenu = await SubmenuCRUD.get_submenu_by_id(db, submenu_id)
        if db_submenu is None:
            return None
        else:
            db_menu = await MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)
            db_menu.submenus_count -= 1
            db_menu.dishes_count -= db_submenu.dishes_count
            await db.delete(db_submenu)
            await db.commit()
            return True

    @staticmethod
    async def update_submenu(db: AsyncSession, submenu_id: int):
        """Update submenu item"""
        await db.commit()
        return await SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id)


class DishCRUD:
    @staticmethod
    async def get_dish_by_id(db: AsyncSession, dish_id: int):
        """Get dish by id"""
        return (await db.execute(select(models.Dish).where(models.Dish.id == dish_id))).scalar()

    @staticmethod
    async def get_dish_by_title(db: AsyncSession, dish_title: str):
        """Get dish by title"""
        return (await db.execute(select(models.Dish).where(models.Dish.title == dish_title))).scalar()

    @staticmethod
    async def get_dishes(menu_id: int, submenu_id: int, db: AsyncSession):
        """Get dishes list"""
        return (
            (
                await db.execute(
                    select(models.Dish)
                    .where(models.Dish.menu_id == menu_id)
                    .where(models.Dish.submenu_id == submenu_id)
                )
            )
            .scalars()
            .all()
        )

    @staticmethod
    async def create_dish(db: AsyncSession, dish: schemes.DishBase, menu_id: int, submenu_id: int):
        """Create dish item"""
        db_dish = models.Dish(**dish.dict())
        db_dish.menu_id = menu_id
        db_dish.submenu_id = submenu_id
        (await MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)).dishes_count += 1
        (await SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id)).dishes_count += 1
        db.add(db_dish)
        await db.commit()
        return db_dish

    @staticmethod
    async def delete_dish(db: AsyncSession, dish_id: int, menu_id: int, submenu_id: int):
        """Delete dish item"""
        db_dish = await DishCRUD.get_dish_by_id(db, dish_id)
        if db_dish is None:
            return None
        else:
            (await MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)).dishes_count -= 1
            (await SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id)).dishes_count -= 1
            await db.delete(db_dish)
            await db.commit()
            return True

    @staticmethod
    async def update_dish(db: AsyncSession, dish_id: int):
        """Update dish item"""
        await db.commit()
        return await DishCRUD.get_dish_by_id(db=db, dish_id=dish_id)


class FillMenu:
    @staticmethod
    async def fill(db: AsyncSession):
        """Fills database with test data from menu.json"""
        async with aiofiles.open("menuapp/menu.json") as f:
            content = await f.read()
        x = json.loads(content)

        for menu in x[0]:
            db_menu = models.Menu(**menu)
            db.add(db_menu)

        for submenu in x[1]:
            db_submenu = models.Submenu(**submenu)
            db.add(db_submenu)

        for dish in x[2]:
            db_dish = models.Dish(**dish)
            db.add(db_dish)
        await db.commit()

        return True


class CreateXL:
    status = None

    @staticmethod
    async def create_xl(db: AsyncSession):
        """Gets database data and sends it to Celery to generate excel file"""
        res = (
            await db.execute(
                select(
                    models.Menu.title,
                    models.Menu.description,
                    models.Menu.dishes_count,
                    models.Submenu.title,
                    models.Submenu.description,
                    models.Submenu.dishes_count,
                    models.Dish.title,
                    models.Dish.description,
                    models.Dish.price,
                )
                .join(models.Submenu, models.Dish.submenu_id == models.Submenu.id)
                .join(models.Menu, models.Dish.menu_id == models.Menu.id)
            )
        ).all()
        res = [tuple(row) for row in res]
        CreateXL.status = to_excel.delay(res)

    @staticmethod
    async def get_xl():
        if CreateXL.status:
            if CreateXL.status.status == "SUCCESS":
                headers = {"Content-Disposition": "attachment; filename=test_menu.xlsx"}
                return FileResponse(
                    "output/test_menu.xlsx",
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers=headers,
                )
            else:
                return {"status": f"{CreateXL.status.status}", "message": "Please wait"}
        else:
            return {"status": False, "message": "Please request to generate excel file first"}
