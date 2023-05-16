from pydantic import BaseModel
from decimal import *
from typing import List
from schemas.ingredient import RecipeIngredient


class MenuBase(BaseModel):
    id: int
    name: str


# For adding a menu orders
class MenuOrderAdd(BaseModel):
    id: int
    qty: int


class MenuOrder(MenuBase):
    qty: int
    ingredients: List[RecipeIngredient]


class Menu(MenuBase):
    price: Decimal
    stock: int

    class Config:
        orm_mode = True


class MenuStatus(BaseModel):
    status: str
