from fastapi import status
from fastapi.testclient import TestClient

from app.api.api_v1.menu import SUBMENU_NOT_F, TITLE_REGISTERED
from app.crud import DEL_SUBMENU_RESULT
from app.tests.data import (data_menu, data_sub_description, data_sub_title,
                            data_submenu, data_up_sub_description,
                            data_up_sub_title, data_up_submenu)


class TestSubmenu:
    def test_not_found(self, client: TestClient):
        menu = client.post("/", json=data_menu)
        menu_id = menu.json()["id"]
        response = client.get(f"/{menu_id}/submenus/not_found")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == SUBMENU_NOT_F

    def test_empty_submenus(self, client: TestClient):
        menu = client.post("/", json=data_menu)
        menu_id = menu.json()["id"]
        response = client.get(f"/{menu_id}/submenus")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_not_duplicate_title(self, client: TestClient):
        menu = client.post("/", json=data_menu)
        menu_id = menu.json()["id"]
        submenu = client.post(f"/{menu_id}/submenus", json=data_submenu)
        assert submenu.status_code == status.HTTP_201_CREATED
        response = client.post(f"/{menu_id}/submenus", json=data_submenu)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == TITLE_REGISTERED

    def test_crud_submenu(self, client):
        menu = client.post("/", json=data_menu)
        menu_id = menu.json()["id"]
        submenu = client.post(f"/{menu_id}/submenus", json=data_submenu)
        assert submenu.status_code == status.HTTP_201_CREATED
        assert submenu.json()["title"] == data_sub_title
        assert submenu.json()["description"] == data_sub_description
        assert "id" in submenu.json()
        submenu_id = submenu.json()["id"]

        response = client.get(f"/{menu_id}/submenus/{submenu_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == submenu_id
        assert response.json()["title"] == data_sub_title
        assert response.json()["description"] == data_sub_description

        submenu = client.patch(
            f"/{menu_id}/submenus/{submenu_id}", json=data_up_submenu
        )
        assert submenu.status_code == status.HTTP_200_OK
        assert submenu.json()["title"] == data_up_sub_title
        assert submenu.json()["description"] == data_up_sub_description
        assert "id" in submenu.json()
        assert submenu.json()["id"] == submenu_id

        response = client.get(f"/{menu_id}/submenus/{submenu_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == submenu_id
        assert response.json()["title"] == data_up_sub_title
        assert response.json()["description"] == data_up_sub_description

        response = client.delete(f"/{menu_id}/submenus/{submenu_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == DEL_SUBMENU_RESULT

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
