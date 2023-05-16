from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import List, Annotated
from decimal import *
from random import randint

from dependencies import verify_user_id
from database import get_db, Session
from services.staff import get_staff
from services.menu import get_menu_by_id, get_menu_stock
from services.journal import revert_journal_from_order
from services.order import (
    get_orders_by_status, add_order, get_order_by_id, add_menu_to_order, set_order_status,
    get_orders_by_status_and_staff
)
from schemas.menu import MenuOrderAdd, MenuStatus
from schemas.order import Order, OrderStatus


router = APIRouter(dependencies=[Depends(verify_user_id)], tags=["order"])

@router.post('/order', status_code=status.HTTP_201_CREATED)
def create_order(
        menu_order: MenuOrderAdd,
        x_user_id: Annotated[str | None, Header()] = None,
        db: Session = Depends(get_db)
    ):
    menu = get_menu_by_id(db, menu_order.id)
    # Check that menu exists
    if not menu:
        raise HTTPException(status_code=404, detail='Menu not found')

    staff = get_staff(db, x_user_id)
    # Check that there is stock for this menu
    if get_menu_stock(db, menu) > 0:
        return add_order(db, staff, menu, menu_order.qty)

    raise HTTPException(status_code=409, detail='There is no stock for this menu')


    # order_id = randint(1,100)
    # if (order_id % 2):
    #     return {'id': order_id}
    # else:
    #     raise HTTPException(status_code=409, detail='There is no stock for this menu')


@router.post('/order/cleanup')
def cancel_all_draft_orders(
        x_user_id: Annotated[str | None, Header()] = None,
        db: Session = Depends(get_db)
    ):
    staff = get_staff(db, x_user_id)
    orders = get_orders_by_status_and_staff(db, OrderStatus.draft, staff)
    for order in orders:
        set_order_status(db, order, OrderStatus.cancelled)
        revert_journal_from_order(db, order, staff)


@router.post('/order/{order_id}')
def add_menu(
        order_id: int,
        menu_order: MenuOrderAdd,
        x_user_id: Annotated[str | None, Header()] = None,
        db: Session = Depends(get_db)
    ):
    order = get_order_by_id(db, order_id)
    # Check that order exists
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    menu = get_menu_by_id(db, menu_order.id)
    # Check that menu exists
    if not menu:
        raise HTTPException(status_code=404, detail='Menu not found')

    staff = get_staff(db, x_user_id)
    # Check that order was created by this user
    if order.staff.id != staff.id:
        raise HTTPException(status_code=401, detail='User can not add any Menu item to an order created by other user')

    if get_menu_stock(db, menu) > 0:
        return add_menu_to_order(db, order, menu, menu_order.qty)

    raise HTTPException(status_code=409, detail='There is no stock for this menu')

    # order_id = randint(1,100)
    # if (order_id % 2):
    #     return {}
    # else:
    #     raise HTTPException(status_code=409, detail='There is no stock for this menu')


@router.put('/order/{order_id}')
def update_order(
        order_id: int,
        menu_status: MenuStatus,
        x_user_id: Annotated[str | None, Header()] = None,
        db: Session = Depends(get_db)
    ):
    order = get_order_by_id(db, order_id)
    # Check that order exists
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    order = set_order_status(db, order, menu_status.status)

    # Recover the stock if the order is cancelled
    if (order.status == OrderStatus.cancelled):
        staff = get_staff(db, x_user_id)
        revert_journal_from_order(db, order, staff)

    return {
        'id': order.id,
        'status': order.status,
    }


@router.get('/order', response_model=List[Order])
def get_order_list(
        status: OrderStatus | None = None,
        db: Session = Depends(get_db)
    ):
    return get_orders_by_status(db, status)
    #return [
    #    {
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
    #                    {
    #                        'id': 393,
    #                        'name': 'Peppercorns',
    #                        'unit': 'dl',
    #                        'qty': 4.4,
    #                    },
    #                    {
    #                        'id': 251,
    #                        'name': 'Elderberry',
    #                        'unit': 'l',
    #                        'qty': 7.4,
    #                    },
    #                    {
    #                        'id': 126,
    #                        'name': 'Oyster Sauce',
    #                        'unit': 'l',
    #                        'qty': 0.6,
    #                    },
    #                    {
    #                        'id': 119,
    #                        'name': 'Molasses',
    #                        'unit': 'l',
    #                        'qty': 0,
    #                    },
    #                    {
    #                        'id': 335,
    #                        'name': 'Brown Rice Vinegar',
    #                        'unit': 'ml',
    #                        'qty': 0,
    #                    },
    #                    {
    #                        'id': 355,
    #                        'name': 'Coconut',
    #                        'unit': 'l',
    #                        'qty': 5.4,
    #                    },
    #                    {
    #                        'id': 208,
    #                        'name': 'Cayenne',
    #                        'unit': 'ml',
    #                        'qty': 5.2,
    #                    },
    #                ]
    #            },
    #            {
    #                'id': 2,
    #                'name': "The Kinks",
    #                'qty': 4,
    #                'ingredients': [
    #                    {
    #                        'id': 403,
    #                        'name': 'Raisin',
    #                        'unit': 'l',
    #                        'qty': 5.2,
    #                    },
    #                    {
    #                        'id': 409,
    #                        'name': 'Peas',
    #                        'unit': 'ml',
    #                        'qty': 4.1,
    #                    },
    #                    {
    #                        'id': 92,
    #                        'name': 'Cassia bark',
    #                        'unit': 'cl',
    #                        'qty': 2.6,
    #                    },
    #                    {
    #                        'id': 440,
    #                        'name': 'Coconut Oil',
    #                        'unit': 'l',
    #                        'qty': 1.4,
    #                    },
    #                    {
    #                        'id': 19,
    #                        'name': 'Apple Juice Concentrate',
    #                        'unit': 'l',
    #                        'qty': 5.9,
    #                    },
    #                    {
    #                        'id': 205,
    #                        'name': 'Cloves',
    #                        'unit': 'l',
    #                        'qty': 3.7,
    #                    }
    #                ]
    #            }
    #        ]
    #    },
    #    {
    #        'id': 2,
    #        'items': [
    #            {
    #                'id': 1,
    #                'name': "Radiohead",
    #                'qty': 1,
    #                'ingredients': [
    #                    {
    #                        'id': 15,
    #                        'name': 'Eggs',
    #                        'unit': 'dl',
    #                        'qty': 2.7,
    #                    },
    #                    {
    #                        'id': 393,
    #                        'name': 'Peppercorns',
    #                        'unit': 'dl',
    #                        'qty': 4.4,
    #                    },
    #                    {
    #                        'id': 251,
    #                        'name': 'Elderberry',
    #                        'unit': 'l',
    #                        'qty': 7.4,
    #                    },
    #                    {
    #                        'id': 126,
    #                        'name': 'Oyster Sauce',
    #                        'unit': 'l',
    #                        'qty': 0.6,
    #                    },
    #                    {
    #                        'id': 119,
    #                        'name': 'Molasses',
    #                        'unit': 'l',
    #                        'qty': 0,
    #                    },
    #                    {
    #                        'id': 335,
    #                        'name': 'Brown Rice Vinegar',
    #                        'unit': 'ml',
    #                        'qty': 0,
    #                    },
    #                    {
    #                        'id': 355,
    #                        'name': 'Coconut',
    #                        'unit': 'l',
    #                        'qty': 5.4,
    #                    },
    #                    {
    #                        'id': 208,
    #                        'name': 'Cayenne',
    #                        'unit': 'ml',
    #                        'qty': 5.2,
    #                    },
    #                ]
    #            },
    #        ]
    #    },
    #]


