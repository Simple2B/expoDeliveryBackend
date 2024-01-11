import pytest
from fastapi.testclient import TestClient
from app import schema as s
from config import config
from .test_data import TestData
from fastapi import status

CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_auth(db, client: TestClient, test_data: TestData):
    TEST_USERNAME = test_data.test_users[0].username
    TEST_PASSWORD = test_data.test_users[0].password
    res = client.post("api/auth/token", json={"username": TEST_USERNAME, "password": TEST_PASSWORD})
    assert res.status_code == 200
    token = s.Token.model_validate(res.json())
    assert token.access_token
    assert token.token_type == "bearer"
    header = dict(Authorization=f"Bearer {token.access_token}")
    res = client.get("api/users/me", headers=header)
    assert res.status_code == 200


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_google_auth(db, client: TestClient, test_data: TestData):
    TEST_GOOGLE_MAIL = "somemail@gmail.com"
    request_data = s.GoogleAuthUser(
        email=TEST_GOOGLE_MAIL,
        first_name="John",
        photo_url="https://link_to_file/file.jpeg",
        uid="some-rand-uid",
    ).dict()

    response = client.post("api/auth/google", json=request_data)
    assert response.status_code == status.HTTP_200_OK
    resp_obj = s.Token.parse_obj(response.json())
    assert resp_obj.access_token
