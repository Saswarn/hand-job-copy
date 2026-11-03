import itertools
import logging
import os
import threading
import time
from collections.abc import Generator
from pathlib import Path

import numpy as np
import simplejpeg

from app.core.config import CameraConfig
from app.services.latest import Latest

Frames = Generator[bytes, None, None]  # JPEG frames; close() releases the device

log = logging.getLogger(__name__)


def v4l2_frames(device: str, width: int, height: int, fps: int) -> Frames:
    """Raw MJPEG frames from a V4L2 camera (Arducam or any USB webcam). Linux only."""
    from linuxpy.video.device import Device, VideoCapture  # pyright: ignore[reportMissingModuleSource]  # Linux only

    with Device(device) as cam:
        capture = VideoCapture(cam)
        capture.set_format(width, height, "MJPG")
        capture.set_fps(fps)
        with capture:
            for frame in capture:
                yield bytes(frame)


def fake_frames(width: int, height: int, fps: int, folder: str | None) -> Frames:
    """Dev / test stand-in for the camera: loops *.jpg from `folder`, or a generated test pattern."""
    if folder:
        frames = [p.read_bytes() for p in sorted(Path(folder).glob("*.jpg"))]
        if not frames:
            raise RuntimeError(f"CAMERA_FAKE_DIR has no *.jpg: {folder}")
    else:
        frames = [_test_pattern(width, height, i, 30) for i in range(30)]
    for data in itertools.cycle(frames):
        time.sleep(1 / fps)  # ponytail: ignores loop overhead, fine for dev
        yield data


def _test_pattern(width: int, height: int, i: int, n: int) -> bytes:
    img = np.zeros((height, width, 3), np.uint8)
    img[..., 0] = np.linspace(0, 255, width, dtype=np.uint8)
    img[..., 2] = np.linspace(0, 255, height, dtype=np.uint8)[:, None]
    size = height // 5
    x, y = (width - size) * i // (n - 1), (height - size) // 2
    img[y : y + size, x : x + size] = 255  # square moving left to right
    return simplejpeg.encode_jpeg(img, quality=85)


class Camera:
    """Reads JPEG frames in its own thread and keeps only the newest one in `latest`."""

    def __init__(self, frames: Frames):
        self.latest: Latest[bytes] = Latest()
        self._frames = frames
        self._first = next(frames)  # opens the device now, so a missing camera fails at startup
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, name="camera", daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join(timeout=2)

    def _run(self) -> None:
        try:
            self.latest.put(self._first)
            for data in self._frames:
                if self._stop.is_set():
                    break
                self.latest.put(data)
        except Exception:
            log.exception("camera thread stopped")
        finally:
            self._frames.close()


def open_camera(cfg: CameraConfig) -> Camera:
    """CAMERA_SOURCE=fake -> generated / folder frames (Windows, tests). Anything else -> V4L2 device."""
    cap = cfg.capture
    if os.environ.get("CAMERA_SOURCE") == "fake":
        frames = fake_frames(cap.width, cap.height, cap.fps, os.environ.get("CAMERA_FAKE_DIR"))
    else:
        frames = v4l2_frames(cfg.device, cap.width, cap.height, cap.fps)
    return Camera(frames)
