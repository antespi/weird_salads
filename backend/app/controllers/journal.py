from fastapi import APIRouter, Depends, Header
from typing import Annotated

from dependencies import verify_user_id
from database import get_db, Session
from services.staff import get_staff
from services.journal import add_journal_entry
from schemas.journal import JournalEntry


router = APIRouter(dependencies=[Depends(verify_user_id)], tags=["journal"])


@router.post('/journal/entry', response_model=JournalEntry)
def create_journal_entry(
        entry: JournalEntry,
        x_user_id: Annotated[str | None, Header()] = None,
        db: Session = Depends(get_db)
    ):
    staff = get_staff(db, x_user_id)
    return add_journal_entry(db, entry, staff)
