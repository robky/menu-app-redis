import copy
from random import randint

from fastapi import status
from fastapi.testclient import TestClient

from app.tests.data import data_dish, data_menu, data_submenu


class TestCount:
    def test_right_count(self, client: TestClient):
        datacopy_submenu = copy.deepcopy(data_submenu)
        datacopy_dish = copy.deepcopy(data_dish)

        menu = client.post("/", json=data_menu)
        menu_id = menu.json()["id"]

        count_submenu = randint(2, 10)
        count_dish = randint(2, 25)
        for i_submenu in range(1, count_submenu + 1):
            datacopy_submenu["title"] = f"Title {i_submenu}"
            submenu = client.post(
                f"/{menu_id}/submenus",
                json=datacopy_submenu,
            )
            assert submenu.status_code == status.HTTP_201_CREATED
            submenu_id = submenu.json()["id"]
            for i_dish in range(1, count_dish + 1):
                datacopy_dish["title"] = f"Title {i_dish}"
                dish = client.post(
                    f"/{menu_id}/submenus/{submenu_id}/dishes",
                    json=datacopy_dish,
                )
                assert dish.status_code == status.HTTP_201_CREATED

        response = client.get(f"/{menu_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["submenus_count"] == count_submenu
        assert response.json()["dishes_count"] == count_submenu * count_dish
