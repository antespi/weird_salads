from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from decimal import *

from services.menu import get_menu_by_id, get_menu_cost
from services.journal import add_journal_from_sale
import models, schemas


def _serialize_ingredients(ingredients: List[models.Ingredient]):
    ings: List[schemas.RecipeIngredient] = []
    for ingredient in ingredients:
        ing = schemas.RecipeIngredient(
            id=ingredient.ingredient_id,
            name=ingredient.ingredient.name,
            unit=ingredient.ingredient.unit,
            qty=ingredient.qty,
        )
        ings.append(ing)
    return ings


def _serialize_items(items: List[models.OrderItem]):
    order_items: List[schemas.Order] = []
    for item in items:
        order_item = schemas.OrderItem(
            id=item.menu.id,
            name=item.menu.recipe.name,
            qty=item.qty,
            ingredients=_serialize_ingredients(item.menu.recipe.ingredients)
        )
        order_items.append(order_item)
    return order_items


def get_orders_by_status_and_staff(db: Session, status: str, staff: models.Staff | None = None):
    q = db.query(models.Order).join(models.OrderItem).join(models.Menu).filter(models.Order.status == status)
    if staff:
        q = q.filter(models.Order.staff_id == staff.id)
    return q.all()


def get_orders_by_status(db: Session, status: str):
    # TODO: Pagination
    # https://fastapi.tiangolo.com/tutorial/sql-databases/#read-data
    orders: List[schemas.Order] = []
    for rec in get_orders_by_status_and_staff(db, status):
        order = schemas.Order(
            id=rec.id,
            items=_serialize_items(rec.items),
        )
        orders.append(order)
    return orders


    #        'id': 1,
    #        'items': [
    #            {
    #                'id': 1,
    #                'name': "Radiohead",
    #                'qty': 2,
    #                'ingredients': [
    #                    {
    #                        'id': 15,
    #                        'name': 'Eggs',
    #                        'unit': 'dl',
    #                        'qty': 2.7,
    #                    },

def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def set_order_status(db: Session, order: models.Order, status: schemas.OrderStatus):
    order.status = status
    db.commit()
    return order


def _create_order_item(order: models.Order, menu: models.Menu, qty: int, menu_cost: Decimal):
    return models.OrderItem(
        order_id = order.id,
        menu_id = menu.id,
        qty = qty,
        price_unit = menu.price,
        price_total = qty * menu.price,
        cost_unit = menu_cost,
        cost_total = qty * menu_cost,
    )

def add_menu_to_order(db: Session, order: models.Order, menu: models.Menu, qty: int):
    order_item = None

    # Is this menu already in the Order?
    for i in order.items:
        if i.menu_id == menu.id:
            order_item = i

    if order_item:
        order_item.qty += qty
        order_item.price_total = order_item.qty * order_item.price_unit
        order_item.cost_total = order_item.qty * order_item.cost_unit
    else:
        order_item = _create_order_item(order, menu, qty, get_menu_cost(db, menu))
        db.add(order_item)

    add_journal_from_sale(db, order, menu, qty)
    db.commit()
    db.refresh(order)
    return order


def add_order(db: Session, staff: models.Staff, menu: models.Order, qty: int):
    menu_cost = get_menu_cost(db, menu)
    order = models.Order(
        staff_id= staff.id,
        status=schemas.OrderStatus.draft
    )
    db.add(order)
    db.flush()
    db.refresh(order)

    order_item = _create_order_item(order, menu, qty, get_menu_cost(db, menu))
    db.add(order_item)

    add_journal_from_sale(db, order, menu, qty)
    db.commit()
    db.refresh(order)
    return order
