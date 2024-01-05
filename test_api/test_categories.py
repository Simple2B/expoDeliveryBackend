import pytest

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.testclient import TestClient
from fastapi import status

from app import schema as s
from app import models as m
from config import config
from api.utility import create_categories

from .test_data import TestData


CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_categories(client: TestClient, headers: dict[str, str], test_data: TestData, db: Session):
    create_categories(db=db)
    response = client.get("/api/categories", headers=headers)

    assert response.status_code == status.HTTP_200_OK

    categories = db.scalars(select(m.Category)).all()
    assert categories

    resp_obj = s.CategoryList.model_validate(response.json())
    assert resp_obj
    assert len(resp_obj.categories) == len(categories)

    response = client.get(f"/api/categories/{categories[0].id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    resp_category: s.Category = s.Category.model_validate(response.json())
    assert resp_category
    assert resp_category.name == categories[0].name

    response = client.get("/api/categories/-1", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
