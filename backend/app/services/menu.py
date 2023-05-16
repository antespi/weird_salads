from sqlalchemy.orm import Session
from typing import List

from services.ingredient import get_ingredient_stock
import models, schemas



def get_menu_cost(db: Session, menu: models.Menu):
    costs = []
    for ri in menu.recipe.ingredients:
        costs.append(ri.ingredient.cost * ri.qty)
    return round(sum(costs), 2)


def get_menu_stock(db: Session, menu: models.Menu):
    ratios = []
    for ri in menu.recipe.ingredients:
        current_stock = get_ingredient_stock(db, ri.ingredient)
        if ri.qty: ratios.append(int(current_stock / ri.qty))
    return min(ratios)


def get_menus(db: Session):
    # TODO: Pagination
    # https://fastapi.tiangolo.com/tutorial/sql-databases/#read-data
    menus: List[schemas.Menu] = []
    records = db.query(models.Menu).join(models.Recipe).all()
    for rec in records:
        menu = schemas.Menu(
            id=rec.id,
            name=rec.recipe.name,
            price=rec.price,
            stock=get_menu_stock(db, rec)
        )
        menus.append(menu)

    return menus


def get_menu_by_id(db: Session, menu_id: int):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()

