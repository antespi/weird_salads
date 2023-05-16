from sqlalchemy import Column, Integer, String, Numeric, Enum

from database import Base
from schemas.ingredient import Unit


class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    unit = Column(Enum(Unit))
    cost = Column(Numeric(12, 2))
