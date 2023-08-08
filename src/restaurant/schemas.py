from uuid import UUID

from pydantic import BaseModel


# Схема для модели Menu
class MenuBase(BaseModel):
    title: str
    description: str | None = None
    submenus_count: int | None = None
    dishes_count: int | None = None


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class Menu(MenuBase):
    id: UUID

    class Config:
        from_attributes = True


# Схема для модели Submenu
class SubmenuBase(BaseModel):
    title: str
    description: str | None = None
    dishes_count: int | None = None


class SubmenuCreate(SubmenuBase):
    pass


class SubmenuUpdate(SubmenuBase):
    pass


class Submenu(SubmenuBase):
    id: UUID

    class Config:
        from_attributes = True


# Схема для модели Dish
class DishBase(BaseModel):
    title: str
    description: str | None = None
    price: str


class DishCreate(BaseModel):
    title: str
    description: str | None = None
    price: str


class DishUpdate(DishBase):
    pass


class Dish(DishBase):
    id: UUID

    class Config:
        from_attributes = True
