from fastapi import FastAPI

from app.api.api_v1 import menu

app = FastAPI()

app.include_router(menu.router, prefix="/api/v1/menus")
