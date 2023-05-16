from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import models


def get_ingredients(db: Session):
    # TODO: Pagination
    # https://fastapi.tiangolo.com/tutorial/sql-databases/#read-data
    return db.query(models.Ingredient).order_by(models.Ingredient.name.asc()).all()


def get_ingredient(db: Session, ingredient_id: int):
    return db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()


def get_ingredient_stock(db: Session, ingredient: models.Ingredient):
    return db.query(
        models.JournalItem.ingredient_id,
        func.sum(models.JournalItem.qty).label('qty_total')
    ).filter(models.JournalItem.ingredient_id == ingredient.id
    ).group_by(models.JournalItem.ingredient_id
    ).first()[1]
