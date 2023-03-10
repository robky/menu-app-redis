from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.api_v1 import menu


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Ресторанное меню",
        version="1.3.3",
        description="Это настроенная схема OpenAPI для взаимодействия с меню.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://clck.ru/33RUW5",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI()
app.openapi = custom_openapi

app.include_router(menu.router, prefix="/api/v1/menus")
