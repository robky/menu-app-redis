from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Menu(Base):
    __tablename__ = "menus"
    id = Column(String, primary_key=True, unique=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)

    submenu = relationship(
        "SubMenu", cascade="all, delete", back_populates="menu"
    )


class SubMenu(Base):
    __tablename__ = "submenus"
    id = Column(String, primary_key=True, unique=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    dishes_count = Column(Integer, default=0)
    menu_id = Column(String, ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenu")
    dish = relationship(
        "Dish", cascade="all, delete", back_populates="submenu"
    )


class Dish(Base):
    __tablename__ = "dishes"
    id = Column(String, primary_key=True, unique=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(String, nullable=False)
    submenu_id = Column(String, ForeignKey("submenus.id"))

    submenu = relationship("SubMenu", back_populates="dish")
