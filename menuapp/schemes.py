from pydantic import BaseModel

'''_____________________DISH SCHEMES______________________'''

# Query input model
class DishBase(BaseModel):
    title: str
    description: str | None = None
    price: str | None = None

# Create input model
class DishCreate(DishBase):
    pass

# Update input model
class DishUpdate(DishBase):
    pass

# Output model
class Dish(DishBase):
    id: str

    class Config:
        orm_mode = True

'''_____________________SUBMENU SCHEMES______________________'''

# Query input model
class SubmenuBase(BaseModel):
    title: str
    description: str | None = None

# Create input model
class SubmenuCreate(SubmenuBase):
    dishes_count: int = 0

# Update input model
class SubmenuUpdate(SubmenuBase):
    pass

# Output model
class Submenu(SubmenuBase):
    id: str
    dishes_count: int

    class Config:
        orm_mode = True

'''_____________________MENU SCHEMES______________________'''

# Query input model
class MenuBase(BaseModel):
    title: str
    description: str | None = None


# Create input model
class MenuCreate(MenuBase):
    submenus_count: int = 0
    dishes_count: int = 0

# Update input model
class MenuUpdate(MenuBase):
    pass

# Output model
class Menu(MenuBase):
    id: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True