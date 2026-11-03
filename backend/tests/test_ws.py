import json
import time
from collections.abc import Callable
from typing import Any

from fastapi.testclient import TestClient
from gpiozero import Device
from starlette.testclient import WebSocketTestSession

from app.core.config import load_config
from app.main import app
from app.services.uv import UvService

PINS = load_config().uv_gpio


def pin_states() -> list[bool]:
    factory = Device.pin_factory
    assert factory is not None
    return [bool(factory.pin(p).state) for p in PINS]


def receive_json(ws: WebSocketTestSession) -> dict[str, Any]:
    """Next text message, skipping the JPEG frames in between."""
    while True:
        msg = ws.receive()
        if msg.get("text"):
            return json.loads(msg["text"])


def wait_until(cond: Callable[[], bool], timeout: float = 2.0) -> bool:
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if cond():
            return True
        time.sleep(0.02)
    return False


def test_health() -> None:
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}


def test_ws_streams_jpeg_and_controls_uv() -> None:
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as ws:
            assert receive_json(ws) == {"type": "uv", "channels": [False, False, False]}
            assert ws.receive_bytes()[:2] == b"\xff\xd8"  # JPEG frame

            ws.send_json({"type": "uv_set", "channel": 1, "on": True})
            assert receive_json(ws) == {"type": "uv", "channels": [False, True, False]}
            assert pin_states() == [False, True, False]

            ws.send_json({"type": "uv_set", "channel": 5, "on": True})
            assert receive_json(ws)["type"] == "error"
            ws.send_text("not json")
            assert receive_json(ws)["type"] == "error"
            ws.send_json({"type": "scan_start"})
            assert receive_json(ws)["type"] == "error"

        # frontend gone -> every channel off
        assert wait_until(lambda: pin_states() == [False, False, False])


def test_shutdown_turns_uv_off() -> None:
    with TestClient(app):
        uv: UvService = app.state.uv
        uv.set(0, True)
        assert pin_states()[0]
    assert pin_states() == [False, False, False]
