from sqlalchemy.orm import Session

from models import Staff


def get_staff(db: Session, staff_id: int):
    return db.query(Staff).filter(Staff.id == staff_id).first()


def get_staff_by_pin(db: Session, pin: int):
    return db.query(Staff).filter(Staff.pin == pin).first()

