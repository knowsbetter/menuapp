from sqlalchemy.orm import Session

from . import models, schemes


class MenuCRUD:

    @staticmethod
    def get_menu_by_id(db: Session, menu_id: int):
        """Get menu by id"""
        return db.query(models.Menu).filter(models.Menu.id == menu_id).first()

    @staticmethod
    def get_menu_by_title(db: Session, menu_title: str):
        'Get menu by title'
        return db.query(models.Menu).filter(models.Menu.title == menu_title).first()

    @staticmethod
    def get_menus(db: Session):
        """Get menus list"""
        return db.query(models.Menu).all()

    @staticmethod
    def create_menu(db: Session, menu: schemes.MenuBase):
        """Create menu item"""
        db_menu = models.Menu(**menu.dict())
        db_menu.dishes_count = 0
        db_menu.submenus_count = 0
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        return db_menu

    @staticmethod
    def delete_menu(db: Session, menu_id: int):
        """Delete menu item"""
        db_menu = MenuCRUD.get_menu_by_id(db, menu_id)
        if db_menu is None:
            return None
        else:
            db.delete(db_menu)
            db.commit()
            return True

    @staticmethod
    def update_menu(db: Session, menu_id: int):
        """Update menu item"""
        db.commit()
        return MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)


class SubmenuCRUD:

    @staticmethod
    def get_submenu_by_id(db: Session, submenu_id: int):
        """Get submenu by id"""
        return db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()

    @staticmethod
    def get_submenu_by_title(db: Session, submenu_title: str):
        """Get submenu by title"""
        return db.query(models.Submenu).filter(models.Submenu.title == submenu_title).first()

    @staticmethod
    def get_submenus(menu_id: int, db: Session):
        """Get submenus list"""
        return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()

    @staticmethod
    def create_submenu(db: Session, submenu: schemes.SubmenuBase, menu_id: int):
        """Create submenu item"""
        db_submenu = models.Submenu(**submenu.dict())
        db_submenu.menu_id = menu_id
        db_submenu.dishes_count = 0
        MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id).submenus_count += 1
        db.add(db_submenu)
        db.commit()
        db.refresh(db_submenu)
        return db_submenu

    @staticmethod
    def delete_submenu(db: Session, menu_id: int, submenu_id: int):
        """Delete submenu item"""
        db_submenu = SubmenuCRUD.get_submenu_by_id(db, submenu_id)
        if db_submenu is None:
            return None
        else:
            db_menu = MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id)
            db_menu.submenus_count -= 1
            db_menu.dishes_count -= db_submenu.dishes_count
            db.delete(db_submenu)
            db.commit()
            return True

    @staticmethod
    def update_submenu(db: Session, submenu_id: int):
        """Update submenu item"""
        db.commit()
        return SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id)

    @staticmethod
    def get_submenus_count(db: Session, menu_id):
        """Get submenus list length"""
        return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).count()


class DishCRUD:

    @staticmethod
    def get_dish_by_id(db: Session, dish_id: int):
        """Get dish by id"""
        return db.query(models.Dish).filter(models.Dish.id == dish_id).first()

    @staticmethod
    def get_dish_by_title(db: Session, dish_title: str):
        """Get dish by title"""
        return db.query(models.Dish).filter(models.Dish.title == dish_title).first()

    @staticmethod
    def get_dishes(submenu_id: int, db: Session):
        """Get dishes list"""
        return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all()

    @staticmethod
    def create_dish(db: Session, dish: schemes.DishBase, menu_id: int, submenu_id: int):
        """Create dish item"""
        db_dish = models.Dish(**dish.dict())
        db_dish.submenu_id = submenu_id
        MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id).dishes_count += 1
        SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id).dishes_count += 1
        db.add(db_dish)
        db.commit()
        db.refresh(db_dish)
        return db_dish

    @staticmethod
    def delete_dish(db: Session, dish_id: int, menu_id: int, submenu_id: int):
        """Delete dish item"""
        db_dish = DishCRUD.get_dish_by_id(db, dish_id)
        if db_dish is None:
            return None
        else:
            MenuCRUD.get_menu_by_id(db=db, menu_id=menu_id).dishes_count -= 1
            SubmenuCRUD.get_submenu_by_id(db=db, submenu_id=submenu_id).dishes_count -= 1
            db.delete(db_dish)
            db.commit()
            return True

    @staticmethod
    def update_dish(db: Session, dish_id: int):
        """Update dish item"""
        db.commit()
        return DishCRUD.get_dish_by_id(db=db, dish_id=dish_id)

    @staticmethod
    def get_dishes_count(db: Session, submenu_id):
        """Get dishes list length"""
        return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).count()
