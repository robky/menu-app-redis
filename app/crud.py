from uuid import uuid4

from sqlalchemy.orm import Session

from app import models, schemas

DEL_MENU_RESULT = {"status": True, "message": "The menu has been deleted"}
DEL_SUBMENU_RESULT = {
    "status": True,
    "message": "The submenu has been deleted",
}
DEL_DISH_RESULT = {"status": True, "message": "The dish has been deleted"}


def get_all_menu(db: Session) -> list[models.Menu]:
    return db.query(models.Menu).all()


def create_menu(db: Session, menu: schemas.MenuCreate) -> models.Menu:
    id_menu = str(uuid4())
    db_menu = models.Menu(
        id=id_menu, title=menu.title, description=menu.description
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def get_menu_by_title(db: Session, title: str) -> models.Menu:
    return db.query(models.Menu).filter(models.Menu.title == title).first()


def get_menu_by_id(db: Session, menu_id: str) -> models.Menu:
    return db.get(models.Menu, menu_id)


def patch_menu(
        db: Session, db_menu: models.Menu, menu: schemas.MenuBase
) -> models.Menu:
    update_data = menu.dict(exclude_unset=True)
    update_object(data=update_data, obj=db_menu, db=db)
    return db_menu


def delete_menu(db: Session, db_menu: models.Menu) -> dict[str: bool | str]:
    db.delete(db_menu)
    db.commit()
    return DEL_MENU_RESULT


def get_submenu_by_title(db: Session, title: str) -> models.SubMenu:
    return (
        db.query(models.SubMenu).filter(models.SubMenu.title == title).first()
    )


def get_submenu_by_id(
        db: Session, menu: models.Menu, submenu_id: str
) -> models.SubMenu | None:
    db_submenu = db.get(models.SubMenu, submenu_id)
    if db_submenu and db_submenu.menu_id == menu.id:
        return db_submenu
    return None


def get_all_submenu(db_menu: models.Menu) -> list[models.SubMenu]:
    return db_menu.submenu


def create_submenu(
        db: Session, db_menu: models.Menu, submenu: schemas.MenuCreate
) -> models.SubMenu:
    id_submenu = str(uuid4())
    db_submenu = models.SubMenu(
        id=id_submenu,
        menu=db_menu,
        title=submenu.title,
        description=submenu.description,
    )
    db_menu.submenus_count += 1
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def patch_submenu(
        db: Session, db_submenu: models.SubMenu, submenu: schemas.MenuBase
) -> models.SubMenu:
    update_data = submenu.dict(exclude_unset=True)
    update_object(data=update_data, obj=db_submenu, db=db)
    return db_submenu


def delete_submenu(
        db: Session, db_submenu: models.SubMenu
) -> dict[str: bool | str]:
    db_submenu.menu.dishes_count -= db_submenu.dishes_count
    db_submenu.menu.submenus_count -= 1
    db.delete(db_submenu)
    db.commit()
    return DEL_SUBMENU_RESULT


def update_object(data: dict[str:str], obj: object, db: Session) -> None:
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)


def get_all_dish(db_submenu: models.SubMenu) -> list[models.Dish]:
    return db_submenu.dish


def get_dish_by_title(
        db: Session, db_submenu: models.SubMenu, title: str
) -> models.Dish:
    return (db.query(models.Dish).filter(
        models.Dish.title == title,
        models.Dish.submenu == db_submenu).first())


def create_dish(
        db: Session, db_submenu: models.SubMenu, dish: schemas.DishCreate
) -> models.Dish:
    id_dish = str(uuid4())
    db_dish = models.Dish(
        id=id_dish,
        submenu=db_submenu,
        title=dish.title,
        description=dish.description,
        price=dish.price,
    )
    db_submenu.dishes_count += 1
    db_submenu.menu.dishes_count += 1
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def get_dish_by_id(
        db: Session, submenu: models.SubMenu, dish_id: str
) -> models.Dish | None:
    db_dish = db.get(models.Dish, dish_id)
    if db_dish and db_dish.submenu_id == submenu.id:
        return db_dish
    return None


def patch_dish(
        db: Session, db_dish: models.Dish, dish: schemas.DishBase
) -> models.Dish:
    update_data = dish.dict(exclude_unset=True)
    update_object(data=update_data, obj=db_dish, db=db)
    return db_dish


def delete_dish(db: Session, db_dish: models.Dish) -> dict[str: bool | str]:
    db_dish.submenu.dishes_count -= 1
    db_dish.submenu.menu.dishes_count -= 1
    db.delete(db_dish)
    db.commit()
    return DEL_DISH_RESULT
