import json

from fastapi.testclient import TestClient

from app.redis import get_redis
from app.tests.data import data_dish, data_menu, data_submenu


class TestCache:
    def test_cache(self, client: TestClient):
        cache = get_redis()

        assert cache.exists("menus") == 0
        menus_bd = client.get("")
        assert cache.exists("menus") == 1
        menus_cache = client.get("")
        assert menus_bd.content == menus_cache.content

        new_menu = client.post("", json=data_menu)
        assert cache.exists("menus") == 0

        menu_id = json.loads(new_menu.content)["id"]
        assert cache.exists(f"menu:{menu_id}") == 0
        menu_bd = client.get(f"/{menu_id}")
        assert cache.exists(f"menu:{menu_id}") == 1
        menu_cache = client.get(f"/{menu_id}")
        assert menu_bd.content == menu_cache.content

        assert cache.exists(f"menu:{menu_id}:submenus") == 0
        submenus_bd = client.get(f"/{menu_id}/submenus")
        assert cache.exists(f"menu:{menu_id}:submenus") == 1
        submenus_cache = client.get(f"/{menu_id}/submenus")
        assert submenus_bd.content == submenus_cache.content

        new_submenu = client.post(f"/{menu_id}/submenus", json=data_submenu)
        assert cache.exists(f"menu:{menu_id}:submenus") == 0

        submenu_id = json.loads(new_submenu.content)["id"]
        assert cache.exists(f"submenu:{submenu_id}") == 0
        assert cache.llen(f"menu:{menu_id}:submenu.list") == 0
        submenu_bd = client.get(f"/{menu_id}/submenus/{submenu_id}")
        assert cache.exists(f"submenu:{submenu_id}") == 1
        assert cache.llen(f"menu:{menu_id}:submenu.list") == 1
        submenu_cache = client.get(f"/{menu_id}/submenus/{submenu_id}")
        assert submenu_bd.content == submenu_cache.content

        assert cache.exists(f"submenu:{submenu_id}:dishes") == 0
        dishes_bd = client.get(f"/{menu_id}/submenus/{submenu_id}/dishes")
        assert cache.exists(f"submenu:{submenu_id}:dishes") == 1
        dishes_cache = client.get(f"/{menu_id}/submenus/{submenu_id}/dishes")
        assert dishes_bd.content == dishes_cache.content

        new_dish = client.post(
            f"/{menu_id}/submenus/{submenu_id}/dishes", json=data_dish
        )
        assert cache.exists(f"submenu:{submenu_id}:dishes") == 0

        dish_id = json.loads(new_dish.content)["id"]
        assert cache.exists(f"dish:{dish_id}") == 0
        assert cache.llen(f"menu:{menu_id}:dish.list") == 0
        dish_bd = client.get(
            f"/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
        )
        assert cache.exists(f"dish:{dish_id}") == 1
        assert cache.llen(f"menu:{menu_id}:dish.list") == 1
        dish_cache = client.get(
            f"/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}"
        )
        assert dish_bd.content == dish_cache.content

        client.delete(f"/{menu_id}")
        assert cache.exists("menus") == 0
        assert cache.exists(f"menu:{menu_id}") == 0
        assert cache.exists(f"menu:{menu_id}:submenus") == 0
        assert cache.exists(f"submenu:{submenu_id}") == 0
        assert cache.llen(f"menu:{menu_id}:submenu.list") == 0
        assert cache.exists(f"submenu:{submenu_id}:dishes") == 0
        assert cache.exists(f"dish:{dish_id}") == 0
        assert cache.llen(f"menu:{menu_id}:dish.list") == 0
