from pydantic import BaseModel
from enum import Enum
from typing import List, Optional
from .ingredient import Ingredient


class JournalSource(str, Enum):
    delivery = 'delivery'
    sale = 'sale'
    waste = 'waste'
    stock = 'stock'


class JournalItem(BaseModel):
    ingredient: Ingredient
    qty: int

    class Config:
        orm_mode = True


class JournalEntry(BaseModel):
    ref: Optional[str]
    source: JournalSource
    items: List[JournalItem]

    class Config:
        orm_mode = True
