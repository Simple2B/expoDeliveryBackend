import pytest
from typing import Sequence

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.testclient import TestClient
from fastapi import status

from app import schema as s
from app import models as m
from config import config
from api.utility import create_categories, create_restaurants, create_restaurants_rates

from .test_data import TestData


CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_restaurant(
    client: TestClient, headers: dict[str, str], test_data: TestData, db: Session
):
    create_categories(db=db)
    create_restaurants(db=db)

    restaurants: Sequence[m.Restaurant] = db.scalars(select(m.Restaurant)).all()
    assert restaurants

    restaurant = restaurants[0]

    response = client.get(f"/api/restaurants/{restaurant.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK

    resp_obj = s.Restaurant.model_validate(response.json())
    assert resp_obj
    assert resp_obj.name == restaurant.name
    assert resp_obj.description == restaurant.description
    assert resp_obj.location == restaurant.location

    create_restaurants_rates(db=db)

    assert restaurant.rates != resp_obj.rates

    response = client.get(f"/api/restaurants/{restaurant.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK

    resp_obj = s.Restaurant.model_validate(response.json())
    assert resp_obj
    assert restaurant.rates == resp_obj.rates

    response = client.get("/api/restaurants/-1", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.get("/api/restaurants/panels", headers=headers)
    assert response.status_code == status.HTTP_200_OK

    resp_panels: s.PanelRestaurantList = s.PanelRestaurantList.from_orm(response.json())
    assert resp_panels
    assert len(resp_panels.panels) == len(restaurants)
