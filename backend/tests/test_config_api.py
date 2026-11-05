from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.config import AppConfig, load_config
from app.main import app


def test_get_config_returns_loaded_file() -> None:
    with TestClient(app) as client:
        response = client.get("/config")
        assert response.status_code == 200
        actual = AppConfig.model_validate(response.json())

    assert actual == load_config()


def test_put_config_saves_and_updates_state(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    original = load_config()
    config_path.write_text(
        original.model_dump_json(indent=2),
        encoding="utf-8",
    )

    with TestClient(app) as client:
        app.state.config_path = config_path

        body = original.model_dump(mode="json")
        body["dirt_conf"] = 0.7 if original.dirt_conf != 0.7 else 0.6
        expected = AppConfig.model_validate(body)

        response = client.put("/config", json=body)

        assert response.status_code == 204
        assert response.content == b""

        actual = AppConfig.model_validate(client.get("/config").json())
        assert actual == expected
        assert load_config(config_path) == expected


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("dirt_conf", 2),
        ("typo", 1),
    ],
)
def test_put_config_rejects_invalid_body(
    tmp_path: Path,
    field: str,
    value: int,
) -> None:
    config_path = tmp_path / "config.json"
    original = load_config()
    config_path.write_text(
        original.model_dump_json(indent=2),
        encoding="utf-8",
    )
    original_bytes = config_path.read_bytes()

    with TestClient(app) as client:
        app.state.config_path = config_path

        body = original.model_dump(mode="json")
        body[field] = value

        response = client.put("/config", json=body)

        assert response.status_code == 422
        assert config_path.read_bytes() == original_bytes

        actual = AppConfig.model_validate(client.get("/config").json())
        assert actual == original