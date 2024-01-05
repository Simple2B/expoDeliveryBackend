from typing import Sequence, cast

from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models as m
from app.logger import log
from .create_rate import create_restaurant_rates

restaurants = [
    {
        "id": 4,
        "name": "Live Cake",
        "rating": "4.9 Excellent",
        "ratings": "(920+)",
        "distance": "1 km away",
        "img": "../images/restaurants/vapiano.png",
        "tags": ["pancakes", "sweets", "waffles"],
        "duration": "35 - 45",
        "location": "Kiev, Ukraine",
    },
    {
        "id": 3,
        "name": "El Molino",
        "rating": "4.9 Excellent",
        "ratings": "(900+)",
        "distance": "0.7 km away",
        "img": "../images/restaurants/molino.png",
        "tags": ["pancakes", "sweets", "waffles"],
        "duration": "35 - 45",
        "location": "Kiev, Ukraine",
    },
    {
        "id": 1,
        "name": "Vapiano",
        "rating": "4.8 Excellent",
        "ratings": "(500+)",
        "distance": "1.2 km away",
        "img": "../images/restaurants/live_cake.png",
        "tags": ["cakes", "cupcakes", "macarons"],
        "duration": "30 - 45",
        "location": "Kiev, Ukraine",
    },
    {
        "id": 2,
        "name": "Urban Greens",
        "rating": "4.5 Excellent",
        "ratings": "(400+)",
        "distance": "0.7 km away",
        "img": "../images/restaurants/urban_greens.png",
        "tags": ["desserts", "donuts"],
        "duration": "30 - 45",
        "location": "Kiev, Ukraine",
    },
]


def create_restaurants(db: Session):
    db_restaurants: Sequence[str] = db.scalars(select(m.Restaurant.name)).all()

    for restaurant in restaurants:
        if restaurant["name"] in db_restaurants:
            continue

        db_restaurant = m.Restaurant(
            name=restaurant["name"],
            image=restaurant["img"],
            description="",
            duration=restaurant["duration"],
            location="",
        )
        db.add(db_restaurant)

        tags: Sequence[str] = cast(Sequence[str], restaurant["tags"])
        categories: Sequence[m.Category] = db.scalars(select(m.Category).where(m.Category.name.in_(tags))).all()
        for category in categories:
            db.add(m.RestaurantCategory(restaurant_id=db_restaurant.id, category_id=category.id))

        db.commit()
        log(log.INFO, f"Restaurant {restaurant} created")
        create_restaurant_rates(db, db_restaurant.id)
    log(log.INFO, "Restaurants created")
