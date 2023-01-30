from fastapi import status
from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    title: str | None = Field(title="Наименование")
    description: str | None = Field(title="Описание")


class MenuCreate(MenuBase):
    class Config:
        schema_extra = {
            "example": {
                "title": "Горячие блюда",
                "description": "Основное составляющее обеденного стола",
            },
        }


class Menu(MenuBase):
    id: str = Field(title="id меню")
    title: str = Field(title="Наименование меню")
    description: str = Field(title="Описание меню")
    submenus_count: int = Field(title="Количество подменю в меню")
    dishes_count: int = Field(title="Количество блюд в меню")

    class Config:
        orm_mode = True


class SubMenu(MenuBase):
    id: str = Field(title="id подменю")
    title: str = Field(title="Наименование подменю")
    description: str = Field(title="Описание подменю")
    dishes_count: int = Field(title="Количество блюд в подменю")

    class Config:
        orm_mode = True


class SubMenuCreate(MenuBase):
    class Config:
        schema_extra = {
            "example": {
                "title": "Супы",
                "description": (
                    "Жидкое блюдо, в составе которого содержится "
                    "не менее 50% жидкости"
                ),
            },
        }


class DishBase(BaseModel):
    title: str | None
    description: str | None
    price: str | None


class DishCreate(DishBase):
    class Config:
        schema_extra = {
            "example": {
                "title": "Суп харчо",
                "description": "Суп из говядины с рисом и кислым соусом.",
                "price": "152.50",
            },
        }


class Dish(DishBase):
    id: str = Field(title="id блюда")
    title: str = Field(title="Наименование блюда")
    description: str = Field(title="Описание блюда")
    price: str = Field(title="Стоимость блюда")

    class Config:
        orm_mode = True


response_400 = {
    "description": "Наименование уже существуют",
    "content": {
        "application/json": {
            "example": {"detail": "Title already registered"}
        },
    },
}
response_menu_404 = {
    "description": "Меню не найдено",
    "content": {"application/json": {"example": {"detail": "menu not found"}}},
}
response_submenu_404 = {
    "description": "Подменю не найдено",
    "content": {
        "application/json": {"example": {"detail": "submenu not found"}},
    },
}
response_dish_404 = {
    "description": "Блюдо не найдено",
    "content": {"application/json": {"example": {"detail": "dish not found"}}},
}

menu_one = {
    "id": "4d6723c7-3e4b-427c-b116-66904a86eef5",
    "title": "Горячие блюда",
    "description": "Основное составляющее обеденного стола",
    "submenus_count": 3,
    "dishes_count": 12,
}
menu_two = {
    "id": "3ffdfed1-e6c7-4066-b5b4-9dad0cffea22",
    "title": "Холодные закуски",
    "description": (
        "Небольшое по объёму преимущественно холодное " "блюдо первой подачи"
    ),
    "submenus_count": 5,
    "dishes_count": 21,
}

menus_response_example = {
    status.HTTP_200_OK: {
        "description": "Список меню",
        "content": {"application/json": {"example": [menu_one, menu_two]}},
    },
}

menu_response_example = {
    status.HTTP_200_OK: {
        "description": "Конкретное меню",
        "content": {"application/json": {"example": menu_one}},
    },
    status.HTTP_404_NOT_FOUND: response_menu_404,
}

menu_create_response_example = {
    status.HTTP_201_CREATED: {
        "description": "Меню создано",
        "content": {"application/json": {"example": menu_one}},
    },
    status.HTTP_400_BAD_REQUEST: response_400,
}
menu_update_response_example = {
    status.HTTP_200_OK: {
        "description": "Меню изменено",
        "content": {"application/json": {"example": menu_one}},
    },
    status.HTTP_400_BAD_REQUEST: response_400,
    status.HTTP_404_NOT_FOUND: response_menu_404,
}
menu_delete_response_example = {
    status.HTTP_200_OK: {
        "description": "Меню удалено",
        "content": {
            "application/json": {
                "example": {
                    "status": True,
                    "message": "The menu has been deleted",
                },
            },
        },
    },
    status.HTTP_404_NOT_FOUND: response_menu_404,
}

submenu_one = {
    "id": "badd3399-9c8b-47ee-8087-a236561a3ede",
    "title": "Супы",
    "description": (
        "Жидкое блюдо, в составе которого содержится " "не менее 50% жидкости"
    ),
    "dishes_count": 5,
}

submenu_two = {
    "id": "d93fb8d4-9460-42be-80ac-c6eb9a549e94",
    "title": "Блюда из мяса",
    "description": (
        "Это основной источник полноценных жиров, белков, "
        "минеральных веществ и витаминов"
    ),
    "dishes_count": 5,
}

submenus_response_example = {
    status.HTTP_200_OK: {
        "description": "Список подменю",
        "content": {
            "application/json": {"example": [submenu_one, submenu_two]},
        },
    },
}

submenu_response_example = {
    status.HTTP_200_OK: {
        "description": "Конкретное подменю",
        "content": {"application/json": {"example": submenu_one}},
    },
    status.HTTP_404_NOT_FOUND: response_submenu_404,
}

submenu_create_response_example = {
    status.HTTP_201_CREATED: {
        "description": "Подменю создано",
        "content": {"application/json": {"example": submenu_one}},
    },
    status.HTTP_400_BAD_REQUEST: response_400,
    status.HTTP_404_NOT_FOUND: response_submenu_404,
}
submenu_update_response_example = {
    status.HTTP_200_OK: {
        "description": "Подменю изменено",
        "content": {"application/json": {"example": submenu_one}},
    },
    status.HTTP_400_BAD_REQUEST: response_400,
    status.HTTP_404_NOT_FOUND: response_submenu_404,
}
submenu_delete_response_example = {
    status.HTTP_200_OK: {
        "description": "Подменю удалено",
        "content": {
            "application/json": {
                "example": {
                    "status": True,
                    "message": "The submenu has been deleted",
                },
            },
        },
    },
    status.HTTP_400_BAD_REQUEST: response_400,
    status.HTTP_404_NOT_FOUND: response_submenu_404,
}

dish_one = {
    "id": "96ec8ff8-1def-4312-8756-7fbec1dc04b1",
    "title": "Суп харчо",
    "description": "Суп из говядины с рисом и кислым соусом.",
    "price": "152.50",
}
dish_two = {
    "id": "147d484c-1239-4354-a711-a363efc8f45a",
    "title": "Суп харчо",
    "description": (
        "Мясной фарш из рубленной баранины, нанизанный на шампур "
        "и зажаренный на мангале."
    ),
    "price": "280.32",
}
dishes_response_example = {
    status.HTTP_200_OK: {
        "description": "Список блюд",
        "content": {"application/json": {"example": [dish_one, dish_two]}},
    },
}

dish_response_example = {
    status.HTTP_200_OK: {
        "description": "Конкретное блюдо",
        "content": {"application/json": {"example": dish_one}},
    },
    status.HTTP_404_NOT_FOUND: response_dish_404,
}

dish_create_response_example = {
    status.HTTP_201_CREATED: {
        "description": "Блюдо создано",
        "content": {"application/json": {"example": dish_one}},
    },
    status.HTTP_400_BAD_REQUEST: response_400,
    status.HTTP_404_NOT_FOUND: response_dish_404,
}
dish_update_response_example = {
    status.HTTP_200_OK: {
        "description": "Блюдо изменено",
        "content": {"application/json": {"example": dish_one}},
    },
    status.HTTP_400_BAD_REQUEST: response_400,
    status.HTTP_404_NOT_FOUND: response_dish_404,
}
dish_delete_response_example = {
    status.HTTP_200_OK: {
        "description": "Блюдо удалено",
        "content": {
            "application/json": {
                "example": {
                    "status": True,
                    "message": "The dish has been deleted",
                },
            },
        },
    },
    status.HTTP_400_BAD_REQUEST: response_400,
    status.HTTP_404_NOT_FOUND: response_dish_404,
}
