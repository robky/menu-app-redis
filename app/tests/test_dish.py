from fastapi import status
from fastapi.testclient import TestClient

from app.api.api_v1.menu import DISH_NOT_F, TITLE_REGISTERED
from app.crud import DEL_DISH_RESULT
from app.tests.data import (
    data_dish,
    data_dish_description,
    data_dish_title,
    data_menu,
    data_price,
    data_submenu,
    data_up_dish,
    data_up_dish_description,
    data_up_dish_title,
    data_up_price,
)


class TestDish:
    def test_not_found(self, client: TestClient):
        menu = client.post("/", json=data_menu)
        menu_id = menu.json()["id"]
        submenu = client.post(f"/{menu_id}/submenus", json=data_submenu)
        submenu_id = submenu.json()["id"]

        response = client.get(
            f"/{menu_id}/submenus/{submenu_id}/dishes/not_found",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == DISH_NOT_F

    def test_empty_dishes(self, client: TestClient):
        menu = client.post("/", json=data_menu)
        menu_id = menu.json()["id"]
        submenu = client.post(f"/{menu_id}/submenus", json=data_submenu)
        submenu_id = submenu.json()["id"]
        response = client.get(f"/{menu_id}/submenus/{submenu_id}/dishes")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_not_duplicate_title(self, client: TestClient):
        menu = client.post("/", json=data_menu)
        menu_id = menu.json()["id"]
        submenu = client.post(f"/{menu_id}/submenus", json=data_submenu)
        submenu_id = submenu.json()["id"]
        dish = client.post(
            f"/{menu_id}/submenus/{submenu_id}/dishes",
            json=data_dish,
        )
        assert dish.status_code == status.HTTP_201_CREATED
        response = client.post(
            f"/{menu_id}/submenus/{submenu_id}/dishes",
            json=data_dish,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == TITLE_REGISTERED

    def test_crud_dish(self, client):
        menu = client.post("/", json=data_menu)
        menu_id = menu.json()["id"]
        submenu = client.post(f"/{menu_id}/submenus", json=data_submenu)
        submenu_id = submenu.json()["id"]
        dish = client.post(
            f"/{menu_id}/submenus/{submenu_id}/dishes",
            json=data_dish,
        )
        assert dish.status_code == status.HTTP_201_CREATED
        assert dish.json()["title"] == data_dish_title
        assert dish.json()["description"] == data_dish_description
        assert dish.json()["price"] == data_price
        assert "id" in dish.json()
        dish_id = dish.json()["id"]

        response = client.get(
            f"/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == dish_id
        assert response.json()["title"] == data_dish_title
        assert response.json()["description"] == data_dish_description
        assert response.json()["price"] == data_price

        dish = client.patch(
            f"/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
            json=data_up_dish,
        )
        assert dish.status_code == status.HTTP_200_OK
        assert dish.json()["title"] == data_up_dish_title
        assert dish.json()["description"] == data_up_dish_description
        assert dish.json()["price"] == data_up_price
        assert "id" in dish.json()
        assert dish.json()["id"] == dish_id

        response = client.get(
            f"/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == dish_id
        assert response.json()["title"] == data_up_dish_title
        assert response.json()["description"] == data_up_dish_description
        assert response.json()["price"] == data_up_price

        response = client.delete(
            f"/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == DEL_DISH_RESULT

        response = client.get(
            f"/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = client.get(f"/{menu_id}/submenus/{submenu_id}/dishes")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

        response = client.delete(f"/{menu_id}/submenus/{submenu_id}")
        assert response.status_code == status.HTTP_200_OK

        response = client.get(f"/{menu_id}/submenus/{submenu_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = client.get(f"/{menu_id}/submenus")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

        response = client.delete(f"/{menu_id}")
        assert response.status_code == status.HTTP_200_OK

        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
