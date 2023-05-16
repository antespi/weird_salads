from typing import Annotated
from fastapi import Header, HTTPException, Depends

from services.staff import get_staff
from database import get_db, Session


def verify_user_id(
        x_user_id: Annotated[str | None, Header()] = None,
        db: Session = Depends(get_db)
    ):
    if not x_user_id:
        raise HTTPException(status_code=401, detail='User PIN is required')

    try:
        x_user_id = int(x_user_id)
    except Exception as ex:
        raise HTTPException(status_code=400, detail='PIN is not a valid number')

    staff = get_staff(db, x_user_id)
    if not staff:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return x_user_id
