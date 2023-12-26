import pytest

from fastapi.testclient import TestClient

from app import schema as s
from config import config

from .test_data import TestData

CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_categories(
    client: TestClient, headers: dict[str, str], test_data: TestData
):
    pass
