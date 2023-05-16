from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base
from schemas.journal import JournalSource


class JournalEntry(Base):
    __tablename__ = "journal_entry"

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))
    ref = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    source = Column(Enum(JournalSource))

    items = relationship("JournalItem", back_populates="entry")
    staff = relationship("Staff")


class JournalItem(Base):
    __tablename__ = "journal_item"

    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("journal_entry.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"))
    qty = Column(Numeric(12, 2))
    cost_unit = Column(Numeric(12, 2))
    cost_total = Column(Numeric(12, 2))

    entry = relationship("JournalEntry", back_populates="items")
    ingredient = relationship("Ingredient")

