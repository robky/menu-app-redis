import pickle

from fastapi import APIRouter, Depends, HTTPException, status
from redis import Redis
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.redis import get_redis

MENU_NOT_F = "menu not found"
SUBMENU_NOT_F = "submenu not found"
DISH_NOT_F = "dish not found"
TITLE_REGISTERED = "Title already registered"

router = APIRouter()


@router.get(
    path="/",
    response_model=list[schemas.Menu],
    responses=schemas.menus_response_example,
    summary="Список меню",
    status_code=status.HTTP_200_OK,
    tags=["Меню"],
)
def read_menus(
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    if cache_data := cache.get("menus"):
        return pickle.loads(cache_data)
    result = crud.get_all_menu(db=db)
    cache.set("menus", pickle.dumps(result))
    return result


@router.post(
    path="/",
    response_model=schemas.Menu,
    responses=schemas.menu_create_response_example,
    summary="Создать меню",
    status_code=status.HTTP_201_CREATED,
    tags=["Меню"],
)
def create_menu(
    menu: schemas.MenuCreate,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    db_menu = crud.get_menu_by_title(db, title=menu.title)
    if db_menu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TITLE_REGISTERED,
        )
    cache.delete("menus")
    return crud.create_menu(db=db, menu=menu)


@router.get(
    path="/{menu_id}",
    response_model=schemas.Menu,
    responses=schemas.menu_response_example,
    summary="Информация по конкретному меню",
    status_code=status.HTTP_200_OK,
    tags=["Меню"],
)
def read_menu(
    menu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    if cache_data := cache.get(f"menu:{menu_id}"):
        return pickle.loads(cache_data)
    result = get_menu_or_404(menu_id=menu_id, db=db)
    cache.set(f"menu:{menu_id}", pickle.dumps(result))
    return result


@router.patch(
    path="/{menu_id}",
    response_model=schemas.Menu,
    responses=schemas.menu_update_response_example,
    summary="Изменить конкретное меню",
    status_code=status.HTTP_200_OK,
    tags=["Меню"],
)
def update_menu(
    menu_id: str,
    menu: schemas.MenuCreate,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    cache.delete(f"menu:{menu_id}")
    cache.delete("menus")
    return crud.patch_menu(db=db, db_menu=db_menu, menu=menu)


@router.delete(
    path="/{menu_id}",
    summary="Удалить меню",
    responses=schemas.menu_delete_response_example,
    status_code=status.HTTP_200_OK,
    tags=["Меню"],
)
def delete_menu(
    menu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    cache.delete("menus")
    cache.delete(f"menu:{menu_id}")
    cache.delete(f"menu:{menu_id}:submenus")
    delete_cache_values(f"menu:{menu_id}:submenu.list", cache)
    delete_cache_values(f"menu:{menu_id}:dish.list", cache)
    return crud.delete_menu(db_menu=db_menu, db=db)


@router.get(
    path="/{menu_id}/submenus",
    response_model=list[schemas.SubMenu],
    responses=schemas.submenus_response_example,
    summary="Список подменю конкретного меню",
    status_code=status.HTTP_200_OK,
    tags=["Подменю"],
)
def read_submenus(
    menu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    if cache_data := cache.get(f"menu:{menu_id}:submenus"):
        return pickle.loads(cache_data)
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    result = crud.get_all_submenu(db_menu=db_menu)
    cache.set(f"menu:{menu_id}:submenus", pickle.dumps(result))
    return result


@router.post(
    path="/{menu_id}/submenus",
    response_model=schemas.SubMenu,
    responses=schemas.submenu_create_response_example,
    summary="Создать подменю в конкретном меню",
    status_code=status.HTTP_201_CREATED,
    tags=["Подменю"],
)
def create_submenu(
    menu_id: str,
    submenu: schemas.SubMenuCreate,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    db_submenu = crud.get_submenu_by_title(db, title=submenu.title)
    if db_submenu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TITLE_REGISTERED,
        )
    cache.delete(f"menu:{menu_id}:submenus")
    return crud.create_submenu(db=db, db_menu=db_menu, submenu=submenu)


@router.get(
    path="/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenu,
    responses=schemas.submenu_response_example,
    summary="Информация по конкретному подменю в конкретном меню",
    status_code=status.HTTP_200_OK,
    tags=["Подменю"],
)
def read_submenu(
    menu_id: str,
    submenu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    if cache_data := cache.get(f"submenu:{submenu_id}"):
        return pickle.loads(cache_data)
    result = get_submenu_or_404(menu_id=menu_id, submenu_id=submenu_id, db=db)
    cache.set(f"submenu:{submenu_id}", pickle.dumps(result))
    cache.rpush(f"menu:{menu_id}:submenu.list", f"submenu:{submenu_id}")
    return result


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}",
    response_model=schemas.SubMenu,
    responses=schemas.submenu_update_response_example,
    summary="Изменить конкретное подменю в конкретном меню",
    status_code=status.HTTP_200_OK,
    tags=["Подменю"],
)
def update_submenu(
    menu_id: str,
    submenu_id: str,
    submenu: schemas.MenuCreate,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    db_submenu = get_submenu_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )
    cache.delete(f"submenu:{submenu_id}")
    cache.delete(f"menu:{menu_id}:submenus")
    return crud.patch_submenu(db=db, db_submenu=db_submenu, submenu=submenu)


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}",
    responses=schemas.submenu_delete_response_example,
    summary="Удалить конкретное подменю в конкретном меню",
    status_code=status.HTTP_200_OK,
    tags=["Подменю"],
)
def delete_submenu(
    menu_id: str,
    submenu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    db_submenu = get_submenu_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )
    cache.delete(f"submenu:{submenu_id}")
    cache.delete(f"menu:{menu_id}")
    cache.delete(f"menu:{menu_id}:submenus")
    cache.delete(f"submenu:{submenu_id}:dishes")

    delete_cache_values(f"submenu:{submenu_id}:dish.list", cache)
    cache.delete("menus")
    return crud.delete_submenu(db_submenu=db_submenu, db=db)


@router.get(
    path="/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=list[schemas.Dish],
    responses=schemas.dishes_response_example,
    summary="Список блюд в конкретном подменю конкретного меню",
    status_code=status.HTTP_200_OK,
    tags=["Блюдо"],
)
def read_dishes(
    menu_id: str,
    submenu_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    if cache_data := cache.get(f"submenu:{submenu_id}:dishes"):
        return pickle.loads(cache_data)
    db_submenu = get_submenu_or_empty_list(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )
    if not db_submenu:
        return db_submenu
    result = crud.get_all_dish(db_submenu=db_submenu)
    cache.set(f"submenu:{submenu_id}:dishes", pickle.dumps(result))
    return result


@router.post(
    path="/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=schemas.Dish,
    responses=schemas.dish_create_response_example,
    summary="Создать блюдо в конкретном подменю конкретного меню",
    status_code=status.HTTP_201_CREATED,
    tags=["Блюдо"],
)
def create_dish(
    menu_id: str,
    submenu_id: str,
    dish: schemas.DishCreate,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    db_submenu = get_submenu_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )
    db_dish = crud.get_dish_by_title(
        db,
        db_submenu=db_submenu,
        title=dish.title,
    )
    if db_dish:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=TITLE_REGISTERED,
        )
    cache.delete(f"submenu:{submenu_id}:dishes")
    cache.delete(f"submenu:{submenu_id}")
    cache.delete(f"menu:{menu_id}")

    return crud.create_dish(db=db, db_submenu=db_submenu, dish=dish)


@router.get(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.Dish,
    responses=schemas.dish_response_example,
    summary="Конкретное блюдо в конкретном подменю конкретного меню",
    status_code=status.HTTP_200_OK,
    tags=["Блюдо"],
)
def read_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    if cache_data := cache.get(f"dish:{dish_id}"):
        return pickle.loads(cache_data)
    result = get_dish_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        db=db,
    )
    cache.set(f"dish:{dish_id}", pickle.dumps(result))
    cache.rpush(f"menu:{menu_id}:dish.list", f"dish:{dish_id}")
    cache.rpush(f"submenu:{submenu_id}:dish.list", f"dish:{dish_id}")
    return result


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=schemas.Dish,
    responses=schemas.dish_update_response_example,
    summary="Изменить конкретное блюдо в конкретном подменю конкретного меню",
    status_code=status.HTTP_200_OK,
    tags=["Блюдо"],
)
def update_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    dish: schemas.DishCreate,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    db_dish = get_dish_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        db=db,
    )
    cache.delete(f"submenu:{submenu_id}:dishes")
    cache.delete(f"dish:{dish_id}")
    return crud.patch_dish(db=db, db_dish=db_dish, dish=dish)


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    responses=schemas.dish_delete_response_example,
    summary="Удалить конкретное блюдо в конкретном подменю конкретного меню",
    status_code=status.HTTP_200_OK,
    tags=["Блюдо"],
)
def delete_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_redis),
):
    db_dish = get_dish_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        db=db,
    )
    cache.delete(f"dish:{dish_id}")
    cache.delete(f"submenu:{submenu_id}:dishes")
    cache.delete(f"submenu:{submenu_id}")
    cache.delete(f"menu:{menu_id}")
    cache.delete("menus")
    return crud.delete_dish(db_dish=db_dish, db=db)


def get_menu_or_404(menu_id: str, db: Session):
    menu = crud.get_menu_by_id(menu_id=menu_id, db=db)
    if menu:
        return menu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=MENU_NOT_F,
    )


def get_submenu_or_404(menu_id: str, submenu_id: str, db: Session):
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    db_submenu = crud.get_submenu_by_id(
        db,
        menu=db_menu,
        submenu_id=submenu_id,
    )
    if db_submenu:
        return db_submenu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=SUBMENU_NOT_F,
    )


def get_submenu_or_empty_list(
    menu_id: str,
    submenu_id: str,
    db: Session,
) -> models.SubMenu | list:
    db_menu = get_menu_or_404(menu_id=menu_id, db=db)
    db_submenu = crud.get_submenu_by_id(
        db,
        menu=db_menu,
        submenu_id=submenu_id,
    )
    if db_submenu:
        return db_submenu
    return []


def get_dish_or_404(menu_id: str, submenu_id: str, dish_id: str, db: Session):
    db_submenu = get_submenu_or_404(
        menu_id=menu_id,
        submenu_id=submenu_id,
        db=db,
    )
    db_dish = crud.get_dish_by_id(db=db, submenu=db_submenu, dish_id=dish_id)
    if db_dish:
        return db_dish
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=DISH_NOT_F,
    )


def delete_cache_values(key_list: str, cache: Redis):
    while value := cache.rpop(key_list):
        cache.delete(value)
