from typing import Sequence

from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models as m
from app.logger import log

categories = [
    "Cakes",
    "Donuts",
    "Cupcakes",
    "Desserts",
    "Sweets",
    "Waffles",
    "Pancakes",
]


def create_categories(db: Session):
    db_categories: Sequence[str] = db.scalars(select(m.Category.name)).all()

    for category in categories:
        if category in db_categories:
            continue

        db_category = m.Category(name=category)
        db.add(db_category)

    db.commit()
    log(log.INFO, f"Categories {categories} created")
