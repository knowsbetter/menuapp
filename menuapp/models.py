from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Menu(Base):
    """Menu data model for database queries"""

    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    submenus_count = Column(Integer, index=True)
    dishes_count = Column(Integer, index=True)

    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan")


class Submenu(Base):
    """Subenu data model for database queries"""

    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"))
    dishes_count = Column(Integer, index=True)

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")


class Dish(Base):
    """Dish data model for database queries"""

    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(String, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"))
    submenu_id = Column(Integer, ForeignKey("submenus.id"))

    submenu = relationship("Submenu", back_populates="dishes")
