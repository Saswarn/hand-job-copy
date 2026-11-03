import os

os.environ["GPIOZERO_PIN_FACTORY"] = "mock"
os.environ["CAMERA_SOURCE"] = "fake"

import json  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402
import simplejpeg  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from gpiozero import Device  # noqa: E402

from app.core.config import load_config  # noqa: E402
from app.main import app  # noqa: E402
from app.utils.image import Box, render_frame  # noqa: E402

PINS = load_config()["uv_gpio"]


def pin_states() -> list[bool]:
    return [bool(Device.pin_factory.pin(p).state) for p in PINS]


def receive_json(ws) -> dict:
    """Next text message, skipping the JPEG frames in between."""
    while True:
        msg = ws.receive()
        if msg.get("text"):
            return json.loads(msg["text"])


def wait_until(cond, timeout: float = 2.0) -> bool:
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if cond():
            return True
        time.sleep(0.02)
    return False


def test_health():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}


def test_ws_streams_jpeg_and_controls_uv():
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as ws:
            assert receive_json(ws) == {"type": "uv", "channels": [False, False, False]}
            assert ws.receive_bytes()[:2] == b"\xff\xd8"  # JPEG frame

            ws.send_json({"type": "uv_set", "channel": 1, "on": True})
            assert receive_json(ws) == {"type": "uv", "channels": [False, True, False]}
            assert pin_states() == [False, True, False]

            ws.send_json({"type": "uv_set", "channel": 5, "on": True})
            assert receive_json(ws)["type"] == "error"
            ws.send_json({"type": "scan_start"})
            assert receive_json(ws)["type"] == "error"

        # frontend gone -> every channel off
        assert wait_until(lambda: pin_states() == [False, False, False])


def test_shutdown_turns_uv_off():
    with TestClient(app) as client:
        client.app.state.uv.set(0, True)
        assert pin_states()[0]
    assert pin_states() == [False, False, False]


def test_render_frame_crops_and_draws_box():
    src = simplejpeg.encode_jpeg(np.full((100, 200, 3), 128, np.uint8), quality=95)
    box = [Box("dirt", 0.9, 0, 0, 1, 1)]

    img = simplejpeg.decode_jpeg(render_frame(src, [0, 0, 0.5, 1], 100, box, 95))
    assert img.shape[:2] == (100, 100)  # left half at full scale: 100 / 0.5 needs the whole 200 px
    r, g, b = img[50, 1]
    assert r > 200 and g < 80  # red dirt box on the left edge
    assert abs(int(img[50, 50, 0]) - 128) < 10  # inside untouched

    img = simplejpeg.decode_jpeg(render_frame(src, [0, 0, 0.5, 1], 50, box, 95))
    assert img.shape[:2] == (50, 50)  # 1/2-scale decode is already wide enough
