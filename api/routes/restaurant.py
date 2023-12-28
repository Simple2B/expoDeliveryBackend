from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import app.models as m
import app.schema as s
from api.dependency import get_db
from app.logger import log

restaurant_router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@restaurant_router.get(
    "/panels", status_code=status.HTTP_200_OK, response_model=s.PanelRestaurantList
)
def get_panels(
    db: Session = Depends(get_db),
):
    log(log.INFO, "Get all restaurants panels")

    restaurants: Sequence[m.Restaurant] = db.scalars(select(m.Restaurant)).all()

    return s.PanelRestaurantList(
        panels=[
            s.PanelRestaurant.model_validate(restaurant) for restaurant in restaurants
        ]
    )


@restaurant_router.get(
    "/{restaurant_id}", status_code=status.HTTP_200_OK, response_model=s.Restaurant
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    log(log.INFO, f"get_restaurant: {restaurant_id}")

    restaurant: m.Restaurant | None = db.scalar(
        select(m.Restaurant).where(m.Restaurant.id == restaurant_id)
    )
    if not restaurant:
        log(log.INFO, "Restaurant [%s] wasn`t found", restaurant_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    return restaurant
