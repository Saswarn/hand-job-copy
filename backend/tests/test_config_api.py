from typing import Any

from fastapi.testclient import TestClient

from app.core.config import load_config
from app.main import app


def test_get_config_returns_loaded_file() -> None:
    with TestClient(app) as client:
        body: dict[str, Any] = client.get("/config").json()
    assert body == load_config().model_dump(mode="json")


def test_put_config_validates_then_is_not_implemented() -> None:
    with TestClient(app) as client:
        good = client.get("/config").json()
        assert client.put("/config", json=good).status_code == 501
        assert client.put("/config", json={**good, "dirt_conf": 2}).status_code == 422
        assert client.put("/config", json={**good, "typo": 1}).status_code == 422
