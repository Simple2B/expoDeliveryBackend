import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

import app.models as m
import app.schema as s
from config import config

from .test_data import TestData

CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_who_am_i(
    client: TestClient,
    db: Session,
    test_data: TestData,
    headers: dict[str, str],
    faker,
):
    user: m.User = db.scalar(select(m.User))
    response = client.get("api/whoami/user", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    resp_obj: s.WhoAmIOut = s.WhoAmIOut.model_validate(response.json())
    assert resp_obj.unique_id == user.unique_id
