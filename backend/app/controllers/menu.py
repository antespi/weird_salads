from fastapi import APIRouter, Depends
from typing import List

from dependencies import verify_user_id
from database import get_db, Session
from services.menu import get_menus
from schemas.menu import Menu


router = APIRouter(dependencies=[Depends(verify_user_id)], tags=["menu"])


@router.get('/menu', response_model=List[Menu])
def get_menu_list(db: Session = Depends(get_db)):
    return get_menus(db)
    #return [
    #    {
    #        'id': 1,
    #        'name': "Radiohead",
    #        'price': 6.15,
    #        'stock': 0
    #    },
    #    {
    #        'id': 2,
    #        'name': "Phish",
    #        'price': 9.42,
    #        'stock': 2
    #    },
    #    {
    #        'id': 3,
    #        'name': "The Jam",
    #        'price': 13.4,
    #        'stock': 3
    #    },
    #    {
    #        'id': 4,
    #        'name': "David Bowie",
    #        'price': 7.75,
    #        'stock': 5
    #    },
    #    {
    #        'id': 5,
    #        'name': "Billy Idol",
    #        'price': 13.16,
    #        'stock': 10
    #    },
    #    {
    #        'id': 6,
    #        'name': "Guns N' Roses",
    #        'price': 2.45,
    #        'stock': 5
    #    },
    #]
