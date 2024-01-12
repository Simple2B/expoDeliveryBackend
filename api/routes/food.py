from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import app.models as m
import app.schema as s
from api.dependency import get_db
from app.logger import log

food_router = APIRouter(prefix="/foods", tags=["Foods"])


@food_router.get("/{food_id}", status_code=status.HTTP_200_OK, response_model=s.Food)
def get_food(
    food_id: int,
    db: Session = Depends(get_db),
):
    log(log.INFO, f"get_food: {food_id}")

    food: m.Food | None = db.scalar(select(m.Food).where(m.Food.id == food_id))
    if not food:
        log(log.INFO, "food [%s] wasn`t found", food_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="food not found",
        )

    return food


@food_router.get("", status_code=status.HTTP_200_OK, response_model=s.FoodList)
def get_foods(
    db: Session = Depends(get_db),
):
    log(log.INFO, "Get all foods")

    foods: Sequence[m.Food] = db.scalars(select(m.Food)).all()

    return s.FoodList(foods=[s.Food.model_validate(food) for food in foods])
