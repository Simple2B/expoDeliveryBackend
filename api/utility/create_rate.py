from typing import Sequence
import random

from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models as m
from app.logger import log

RATES_NUMBER = 50


def create_restaurant_rates(
    db: Session, restaurant_id: int, rates_number: int = RATES_NUMBER
):
    restaurant: m.Restaurant | None = db.scalar(
        select(m.Restaurant).where(m.Restaurant.id == restaurant_id)
    )
    if not restaurant:
        log(log.INFO, "Restaurant [%s] wasn`t found", restaurant_id)
        return

    user: m.User | None = db.scalar(select(m.User).where(m.User.id == 1))
    if not user:
        log(log.INFO, "User [%s] wasn`t found", 1)
        log(log.INFO, "Create user with id [%s]", 1)
        return

    for _ in range(rates_number):
        rate = m.Rate(
            restaurant_id=restaurant_id,
            user_id=user.id,
            rate=random.randint(1, 5),
        )
        db.add(rate)

    db.commit()
    log(log.INFO, f"Rates ({rates_number}) for restaurant {restaurant_id} created")


def create_restaurants_rates(db: Session, rates_number: int = RATES_NUMBER):
    restaurants: Sequence[m.Restaurant] = db.scalars(select(m.Restaurant)).all()

    user: m.User | None = db.scalar(select(m.User).where(m.User.id == 1))
    if not user:
        log(log.INFO, "User [%s] wasn`t found", 1)
        log(log.INFO, "Create user with id [%s]", 1)
        return

    for restaurant in restaurants:
        rates = random.randint(rates_number // 2, rates_number)
        for _ in range(rates):
            rate = m.Rate(
                restaurant_id=restaurant.id,
                user_id=user.id,
                rate=random.randint(1, 5),
            )
            db.add(rate)

        db.commit()
        log(log.INFO, f"Rates ({rates}) for restaurant {restaurant.id} created")
