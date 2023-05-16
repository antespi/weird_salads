from fastapi import APIRouter, Depends
from typing import List

from dependencies import verify_user_id
from database import get_db, Session
from services.ingredient import get_ingredients
from schemas.ingredient import Ingredient

router = APIRouter(dependencies=[Depends(verify_user_id)], tags=["ingredient"])


@router.get('/ingredient', response_model=List[Ingredient])
def get_ingredient_list(db: Session = Depends(get_db)):
    return get_ingredients(db)
    #return [
    #    {
    #        'id': 1,
    #        'name': 'Yoghurt',
    #        'unit': 'dl',
    #    },
    #    {
    #        'id': 2,
    #        'name': 'Arugula',
    #        'unit': 'dl',
    #    },
    #    {
    #        'id': 3,
    #        'name': 'Gula Melaka',
    #        'unit': 'dl',
    #    },
    #    {
    #        'id': 4,
    #        'name': 'Mahlab',
    #        'unit': 'cl',
    #    },
    #    {
    #        'id': 5,
    #        'name': 'Parmesan Cheese',
    #        'unit': 'ml',
    #    },
    #    {
    #        'id': 6,
    #        'name': 'Barberry',
    #        'unit': 'cl',
    #    },
    #    {
    #        'id': 7,
    #        'name': 'Juniper Berries',
    #        'unit': 'cl',
    #    },
    #    {
    #        'id': 8,
    #        'name': 'Lettuce',
    #        'unit': 'l',
    #    },
    #]
