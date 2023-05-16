from sqlalchemy.orm import Session

from services.ingredient import get_ingredient
import schemas, models


def add_journal_entry(db: Session, entry: schemas.JournalEntry, staff: models.Staff):
    journal_entry = models.JournalEntry(
        ref=entry.ref,
        source=entry.source,
        staff_id= staff.id,
    )
    db.add(journal_entry)
    db.flush()
    db.refresh(journal_entry)
    for i in entry.items:
        ingredient = get_ingredient(db, i.ingredient.id)
        journal_item = models.JournalItem(
            entry_id = journal_entry.id,
            ingredient_id = ingredient.id,
            qty = i.qty,
            cost_unit = ingredient.cost,
            cost_total = ingredient.cost * i.qty
        )
        db.add(journal_item)
    db.commit()
    db.refresh(journal_entry)
    return journal_entry


def add_journal_from_sale(db: Session, order: models.Order, menu: models.Menu, qty: int, do_commit: bool = False):
    journal_entry = models.JournalEntry(
        ref=str(order.id),
        source=schemas.JournalSource.sale,
        staff_id= order.staff.id,
    )
    db.add(journal_entry)
    db.flush()
    db.refresh(journal_entry)
    for ri in menu.recipe.ingredients:
        journal_item = models.JournalItem(
            entry_id = journal_entry.id,
            ingredient_id = ri.ingredient_id,
            qty = ri.qty * qty * (-1),
            cost_unit = ri.ingredient.cost,
            cost_total = ri.ingredient.cost * ri.qty * qty * (-1)
        )
        db.add(journal_item)
        db.flush()

    if do_commit:
        db.commit()
    db.refresh(journal_entry)
    return journal_entry

def revert_journal_from_order(db: Session, order: models.Order, staff: models.Staff):
    journal_items = {}
    journal_entry = models.JournalEntry(
        ref=str(order.id),
        source=schemas.JournalSource.sale,
        staff_id= staff.id,
    )
    db.add(journal_entry)
    db.flush()
    db.refresh(journal_entry)
    for i in order.items:
        for ri in i.menu.recipe.ingredients:
            journal_item = journal_items.get(ri.ingredient_id, None)
            if journal_item:
                journal_item.qty += (ri.qty * i.qty)
                journal_item.cost_total += (ri.ingredient.cost * ri.qty * i.qty)
            else:
                journal_item = models.JournalItem(
                    entry_id = journal_entry.id,
                    ingredient_id = ri.ingredient_id,
                    qty = ri.qty * i.qty,
                    cost_unit = ri.ingredient.cost,
                    cost_total = ri.ingredient.cost * ri.qty * i.qty
                )
                journal_items[ri.ingredient_id] = journal_item
    for j in journal_items.values():
        db.add(j)

    db.commit()
    db.refresh(journal_entry)
    return journal_entry
