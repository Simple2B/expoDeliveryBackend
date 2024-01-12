import pytest

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.testclient import TestClient
from fastapi import status

from app import schema as s
from app import models as m
from config import config
from api.utility import create_foods_for_restaurant, create_restaurants, create_categories

from .test_data import TestData


CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_foods(client: TestClient, headers: dict[str, str], test_data: TestData, db: Session):
    create_categories(db)
    create_restaurants(db)
    restaurant: m.Restaurant | None = db.scalar(select(m.Restaurant))
    assert restaurant

    create_foods_for_restaurant(db, restaurant_id=restaurant.id)
    response = client.get("/api/foods", headers=headers)

    assert response.status_code == status.HTTP_200_OK

    foods = db.scalars(select(m.Food)).all()
    assert foods

    resp_obj = s.FoodList.model_validate(response.json())
    assert resp_obj
    assert len(resp_obj.foods) == len(foods)

    response = client.get(f"/api/foods/{foods[0].id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    resp_food: s.Food = s.Food.model_validate(response.json())
    assert resp_food
    assert resp_food.name == foods[0].name

    response = client.get("/api/foods/-1", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
