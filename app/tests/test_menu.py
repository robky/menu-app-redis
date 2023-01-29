from fastapi import status
from fastapi.testclient import TestClient

from app.api.api_v1.menu import MENU_NOT_F, TITLE_REGISTERED
from app.crud import DEL_MENU_RESULT
from app.tests.data import (data_description, data_menu, data_title,
                            data_up_description, data_up_menu, data_up_title)


class TestMenu:
    def test_not_found(self, client: TestClient):
        response = client.get("/not_found")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == MENU_NOT_F

    def test_empty_menus(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_not_duplicate_title(self, client: TestClient):
        response = client.post("/", json=data_menu)
        assert response.status_code == status.HTTP_201_CREATED
        response = client.post("/", json=data_menu)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == TITLE_REGISTERED

    def test_crud_menu(self, client):
        menu = client.post("/", json=data_menu)
        assert menu.status_code == status.HTTP_201_CREATED
        assert menu.json()["title"] == data_title
        assert menu.json()["description"] == data_description
        assert "id" in menu.json()
        menu_id = menu.json()["id"]

        response = client.get(f"/{menu_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == menu_id
        assert response.json()["title"] == data_title
        assert response.json()["description"] == data_description

        menu = client.patch(f"/{menu_id}", json=data_up_menu)
        assert menu.status_code == status.HTTP_200_OK
        assert menu.json()["title"] == data_up_title
        assert menu.json()["description"] == data_up_description
        assert "id" in menu.json()
        assert menu.json()["id"] == menu_id

        response = client.get(f"/{menu_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == menu_id
        assert response.json()["title"] == data_up_title
        assert response.json()["description"] == data_up_description

        response = client.delete(f"/{menu_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == DEL_MENU_RESULT

        response = client.get(f"/{menu_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
