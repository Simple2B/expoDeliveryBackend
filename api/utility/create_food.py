import random

from faker import Faker
from typing import Sequence

from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models as m
from app.logger import log

NUMBER_OF_FOODS = 5

foods = [
    {"name": "Vanilla Cake", "image": "../images/restaurants/cakes/vanilla_cake.png"},
    {"name": "Strawberry Cake", "image": "../images/restaurants/cakes/strawberry_cake.png"},
    {"name": "Chocolate Cake", "image": "../images/restaurants/cakes/chocolate_cake.png"},
]

faker: Faker = Faker()


def create_foods_for_restaurant(db: Session, restaurant_id: int):
    restaurant: m.Restaurant | None = db.scalar(select(m.Restaurant).where(m.Restaurant.id == restaurant_id))

    if not restaurant:
        log(log.INFO, "restaurant [%s] wasn`t found", restaurant_id)
        return

    categories = db.scalars(select(m.Category)).all()
    counter = 0

    for food in foods:
        for count in range(random.randint(1, NUMBER_OF_FOODS)):
            db_food = m.Food(
                name=food["name"] + str(count),
                calories=random.randint(100, 1000),
                price=round(random.uniform(1, 15), 2),
                image="../images/restaurants/cakes/chocolate_cake.png",
                restaurant_id=restaurant_id,
                info=faker.text(),
            )

            db.add(db_food)
            db.flush()
            for _ in range(random.randint(1, 3)):
                category = random.choice(categories)
                db_food_category = m.FoodTags(
                    food_id=db_food.id,
                    category_id=category.id,
                )
                db.add(db_food_category)
            db.commit()
        counter += count + 1

    db.commit()
    log(log.INFO, f"Foods ({counter}) created")
