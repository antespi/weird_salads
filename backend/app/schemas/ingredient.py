from pydantic import BaseModel
from enum import Enum
from decimal import *


class Unit(str, Enum):
    l = 'l'
    dl = 'dl'
    cl = 'cl'
    ml = 'ml'


class IngredientBase(BaseModel):
    id: int
    name: str
    unit: Unit


class RecipeIngredient(IngredientBase):
    qty: int


class Ingredient(IngredientBase):
    class Config:
        orm_mode = True
