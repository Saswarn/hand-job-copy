import threading
from pathlib import Path

import pytest
from gpiozero import Device

from app.services.camera import Camera, fake_frames
from app.services.latest import Latest
from app.services.uv import UvService

PINS = (5, 6, 13)  # not the config pins, so this never clashes with the app's UvService


def pin_states() -> list[bool]:
    factory = Device.pin_factory
    assert factory is not None
    return [bool(factory.pin(p).state) for p in PINS]


def test_latest_returns_newest_and_times_out() -> None:
    latest: Latest[str] = Latest()
    assert latest.wait_newer(0, timeout=0.01) == (0, None)
    latest.put("a")
    latest.put("b")
    assert latest.wait_newer(0, timeout=0.01) == (2, "b")  # "a" was dropped, not queued
    assert latest.wait_newer(2, timeout=0.01) == (2, None)


def test_latest_wakes_waiting_thread() -> None:
    latest: Latest[int] = Latest()
    threading.Timer(0.05, latest.put, args=(7,)).start()
    assert latest.wait_newer(0, timeout=2) == (1, 7)


def test_uv_starts_off_and_close_turns_off() -> None:
    uv = UvService(PINS)
    try:
        assert uv.state() == [False, False, False]
        uv.set(2, True)
        assert uv.state() == [False, False, True]
        assert pin_states() == [False, False, True]
        uv.all_off()
        assert pin_states() == [False, False, False]
        uv.set(0, True)
    finally:
        uv.close()
    assert pin_states() == [False, False, False]


def test_fake_frames_loops_folder(tmp_path: Path) -> None:
    (tmp_path / "b.jpg").write_bytes(b"B")
    (tmp_path / "a.jpg").write_bytes(b"A")
    frames = fake_frames(1, 1, 1000, str(tmp_path))
    assert [next(frames) for _ in range(3)] == [b"A", b"B", b"A"]
    frames.close()


def test_fake_frames_empty_folder_fails(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="no \\*.jpg"):
        next(fake_frames(1, 1, 30, str(tmp_path)))


def test_camera_keeps_newest_frame() -> None:
    camera = Camera(fake_frames(64, 36, 1000, None))
    camera.start()
    try:
        seq, jpeg = camera.latest.wait_newer(0, timeout=2)
        assert seq >= 1 and jpeg is not None and jpeg[:2] == b"\xff\xd8"
    finally:
        camera.stop()
