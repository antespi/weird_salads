from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from database import Base


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    ingredients = relationship("RecipeIngredient", back_populates="recipe")


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    price = Column(Numeric(12, 2))

    recipe = relationship("Recipe")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"))
    qty = Column(Numeric(12, 2))

    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient")

