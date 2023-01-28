from pydantic import BaseModel

'''_____________________DISH SCHEMES______________________'''

# Query input model
class DishBase(BaseModel):
    title: str
    description: str | None = None
    price: str | None = None

    class Config:
        schema_extra = {
            'example': {
                'title': 'dish title',
                'descrition': 'dish description',
                'price': '0.00',
            }
        }

# Create input model
class DishCreate(DishBase):
    pass

# Update input model
class DishUpdate(BaseModel):
    title: str
    description: str | None = None
    price: str | None = None

    class Config:
        schema_extra = {
            'example': {
                'title': 'updated dish title',
                'descrition': 'updated dish description',
                'price': '0.00',
            }
        }

# Output model
class Dish(DishBase):
    id: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'dish title',
                'descrition': 'dish description',
                'price': 'dish price',
                'id': 'dish id'
            }
        }

# Delete output model
class DishDelete(BaseModel):
    status: bool
    message: str

    class Config:
        schema_extra = {
            'example': {
                'status': 'status',
                'message': 'message'
            }
        }

'''_____________________SUBMENU SCHEMES______________________'''

# Query input model
class SubmenuBase(BaseModel):
    title: str
    description: str | None = None

    class Config:
        schema_extra = {
            'example': {
                'title': 'submenu title',
                'descrition': 'submenu description',
            }
        }

# Create input model
class SubmenuCreate(SubmenuBase):
    dishes_count: int = 0

# Update input model
class SubmenuUpdate(BaseModel):
    title: str
    description: str | None = None

    class Config:
        schema_extra = {
            'example': {
                'title': 'updated submenu title',
                'descrition': 'updated submenu description',
            }
        }

# Output model
class Submenu(SubmenuBase):
    id: str
    dishes_count: int

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'submenu title',
                'descrition': 'submenu description',
                'id': 'submenu id',
                'dishes_count': 'number of dishes'
            }
        }

# Delete output model
class SubmenuDelete(BaseModel):
    status: bool
    message: str

    class Config:
        schema_extra = {
            'example': {
                'status': 'status',
                'message': 'message'
            }
        }

'''_____________________MENU SCHEMES______________________'''

# Query input model
class MenuBase(BaseModel):
    title: str
    description: str | None = None

    class Config:
        schema_extra = {
            'example': {
                'title': 'menu title',
                'descrition': 'menu description',
            }
        }

# Create input model
class MenuCreate(MenuBase):
    submenus_count: int = 0
    dishes_count: int = 0

# Update input model
class MenuUpdate(BaseModel):
    title: str
    description: str | None = None

    class Config:
        schema_extra = {
            'example': {
                'title': 'updated menu title',
                'descrition': 'updated menu description',
            }
        }

# Output model
class Menu(MenuBase):
    id: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'menu title',
                'descrition': 'menu description',
                'id': 'menu id',
                'submenu_count': 'number of submenus',
                'dishes_count': 'number of dishes'
            }
        }

# Delete output model
class MenuDelete(BaseModel):
    status: bool
    message: str

    class Config:
        schema_extra = {
            'example': {
                'status': 'status',
                'message': 'message'
            }
        }
