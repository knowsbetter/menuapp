from pydantic import BaseModel


class DishBase(BaseModel):
    """Scheme for input data for dish item creation"""

    title: str
    description: str | None = None
    price: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "title": "dish title",
                "description": "dish description",
                "price": "0.00",
            }
        }


class DishUpdate(BaseModel):
    """Scheme for input data for dish item update"""

    title: str
    description: str | None = None
    price: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "title": "updated dish title",
                "description": "updated dish description",
                "price": "0.00",
            }
        }


class Dish(DishBase):
    """Scheme for output dish information"""

    id: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "dish title",
                "description": "dish description",
                "price": "dish price",
                "id": "dish id",
            }
        }


class DishDelete(BaseModel):
    """Scheme for dish removal response"""

    status: bool
    message: str

    class Config:
        schema_extra = {"example": {"status": "status", "message": "message"}}


class SubmenuBase(BaseModel):
    """Scheme for input data for submenu item creation"""

    title: str
    description: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "title": "submenu title",
                "description": "submenu description",
            }
        }


class SubmenuUpdate(BaseModel):
    """Scheme for input data for submenu item update"""

    title: str
    description: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "title": "updated submenu title",
                "description": "updated submenu description",
            }
        }


class Submenu(SubmenuBase):
    """Scheme for output submenu information"""

    id: str
    dishes_count: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "submenu title",
                "description": "submenu description",
                "id": "submenu id",
                "dishes_count": "number for dishes",
            }
        }


class SubmenuDelete(BaseModel):
    """Scheme for submenu removal response"""

    status: bool
    message: str

    class Config:
        schema_extra = {"example": {"status": "status", "message": "message"}}


class MenuBase(BaseModel):
    """Scheme for input data for menu item creation"""

    title: str
    description: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "title": "menu title",
                "description": "menu description",
            }
        }


class MenuUpdate(BaseModel):
    """Scheme for input data for menu item update"""

    title: str
    description: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "title": "updated menu title",
                "description": "updated menu description",
            }
        }


class Menu(MenuBase):
    """Scheme for output menu information"""

    id: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "menu title",
                "description": "menu description",
                "id": "menu id",
                "submenu_count": "number for submenus",
                "dishes_count": "number for dishes",
            }
        }


class MenuDelete(BaseModel):
    """Scheme for submenu removal response"""

    status: bool
    message: str

    class Config:
        schema_extra = {"example": {"status": "status", "message": "message"}}


class Password(BaseModel):
    """Input scheme for special features"""

    password: str

    class Config:
        schema_extra = {"example": {"password": "12345"}}
