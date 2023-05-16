from pydantic import BaseModel
from enum import Enum
from typing import List
from schemas.ingredient import RecipeIngredient


class OrderStatus(str, Enum):
    draft = 'draft'
    paid = 'paid'
    done = 'done'
    cancelled = 'cancelled'


class OrderItem(BaseModel):
    id: int
    name: str
    qty: int
    ingredients: List[RecipeIngredient]


class Order(BaseModel):
    id: int
    items: List[OrderItem]
