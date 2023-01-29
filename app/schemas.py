from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str | None
    description: str | None


class MenuCreate(MenuBase):
    title: str
    description: str


class Menu(MenuBase):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class SubMenu(MenuBase):
    id: str
    title: str
    description: str
    dishes_count: int

    class Config:
        orm_mode = True


class DishBase(BaseModel):
    title: str | None
    description: str | None
    price: str | None


class DishCreate(DishBase):
    title: str
    description: str
    price: str


class Dish(DishBase):
    id: str
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
