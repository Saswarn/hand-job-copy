import time
from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient
from gpiozero import Device
from pydantic import TypeAdapter
from starlette.testclient import WebSocketTestSession

from app.core.config import load_config
from app.main import app
from app.services.detector import Detector
from app.services.uv import UvService
from app.utils.image import Box

PINS = load_config().uv_gpio
_json_message = TypeAdapter(dict[str, object])


def pin_states() -> list[bool]:
    factory = Device.pin_factory
    assert factory is not None
    return [bool(factory.pin(p).state) for p in PINS]


def receive_json(ws: WebSocketTestSession) -> dict[str, object]:
    """Next text message, skipping the JPEG frames in between."""
    while True:
        msg = ws.receive()
        text = msg.get("text")
        if isinstance(text, str):
            return _json_message.validate_json(text)


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
            ws.send_json({"type": "binary_view", "on": True})
            assert receive_json(ws)["type"] == "error"

        # frontend gone -> every channel off
        assert wait_until(lambda: pin_states() == [False, False, False])


def test_shutdown_turns_uv_off() -> None:
    with TestClient(app):
        uv: UvService = app.state.uv
        uv.set(0, True)
        assert pin_states()[0]
    assert pin_states() == [False, False, False]


class FixedDetector(Detector):
    def __init__(self, boxes: list[Box]) -> None:
        self.boxes = boxes

    def latest(self) -> list[Box]:
        return list(self.boxes)


class FailingDetector(Detector):
    def latest(self) -> list[Box]:
        raise ValueError("detector failed")


def start_scan(ws: WebSocketTestSession) -> None:
    assert receive_json(ws) == {"type": "uv", "channels": [False, False, False]}
    ws.send_json({"type": "scan_start"})
    assert receive_json(ws) == {"type": "uv", "channels": [True, True, True]}


@pytest.mark.parametrize("dirty", [False, True])
def test_scan_counts_down_and_finishes_with_uv_off(dirty: bool) -> None:
    boxes = [Box("dirt", 0.9, 0.1, 0.1, 0.2, 0.2)] if dirty else []
    with TestClient(app) as client:
        app.state.config = load_config().model_copy(update={"scan_seconds": 1.05})
        app.state.detector = FixedDetector(boxes)
        with client.websocket_connect("/ws") as ws:
            start_scan(ws)
            remaining_values: list[float] = []
            while True:
                message = receive_json(ws)
                if message.get("state") == "done":
                    assert message == {
                        "type": "scan", "state": "done", "remaining_s": None,
                        "result": "dirt" if dirty else "clean",
                    }
                    assert pin_states() == [False, False, False]
                    break
                assert message["state"] == "scanning"
                assert message["result"] is None
                remaining = message["remaining_s"]
                assert isinstance(remaining, (float, int))
                assert 0 <= remaining <= 1.05
                remaining_values.append(float(remaining))
                assert pin_states() == [True, True, True]
            assert len(remaining_values) >= 3
            assert remaining_values == sorted(remaining_values, reverse=True)
            assert receive_json(ws) == {"type": "uv", "channels": [False, False, False]}


def test_disconnect_during_scan_turns_uv_off() -> None:
    with TestClient(app) as client:
        app.state.config = load_config().model_copy(update={"scan_seconds": 10.0})
        app.state.detector = FixedDetector([])
        with client.websocket_connect("/ws") as ws:
            start_scan(ws)
            assert receive_json(ws)["state"] == "scanning"
            assert pin_states() == [True, True, True]
        assert wait_until(lambda: pin_states() == [False, False, False])
        # A cancelled scan must not turn the lights back on later.
        with client.websocket_connect("/ws") as ws:
            assert receive_json(ws) == {"type": "uv", "channels": [False, False, False]}


def test_duplicate_scan_is_rejected_and_other_messages_still_work() -> None:
    with TestClient(app) as client:
        app.state.config = load_config().model_copy(update={"scan_seconds": 0.2})
        with client.websocket_connect("/ws") as ws:
            start_scan(ws)
            assert receive_json(ws)["state"] == "scanning"
            ws.send_json({"type": "scan_start"})
            assert receive_json(ws) == {"type": "error", "message": "scan already in progress"}
            ws.send_json({"type": "uv_set", "channel": 0, "on": False})
            assert receive_json(ws) == {"type": "uv", "channels": [False, True, True]}
            assert receive_json(ws)["state"] == "done"
            assert receive_json(ws) == {"type": "uv", "channels": [False, False, False]}
            # A completed task must not block the next scan.
            ws.send_json({"type": "scan_start"})
            assert receive_json(ws) == {"type": "uv", "channels": [True, True, True]}
            assert receive_json(ws)["state"] == "scanning"


def test_detector_error_turns_uv_off_and_reports_error() -> None:
    with TestClient(app) as client:
        app.state.detector = FailingDetector()
        with client.websocket_connect("/ws") as ws:
            start_scan(ws)
            assert receive_json(ws) == {"type": "error", "message": "scan failed"}
            assert pin_states() == [False, False, False]
            assert receive_json(ws) == {"type": "uv", "channels": [False, False, False]}
