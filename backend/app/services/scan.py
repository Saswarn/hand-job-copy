from collections.abc import Sequence
from typing import Literal

from app.utils.image import Box

ScanResult = Literal["clean", "dirt"]


def judge(frames: Sequence[Sequence[Box]], dirt_conf: float, dirt_min_frames: int) -> ScanResult:
    """Scan result from the detections of every frame in one scan, oldest first.

    Rule (systems/spec/backend.md §Scan logic): "dirt" when a box with cls "dirt" and
    conf >= dirt_conf appears in >= dirt_min_frames frames in a row, else "clean".

    TODO(backend): implement as a pure function (no camera / GPIO / time) + tests in tests/test_scan.py.
    """
    raise NotImplementedError
