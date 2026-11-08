from collections.abc import Sequence
from typing import Literal

from app.utils.image import Box

ScanResult = Literal["clean", "dirt"]


def judge(frames: Sequence[Sequence[Box]], dirt_conf: float, dirt_min_frames: int) -> ScanResult:
    """Scan result from the detections of every frame in one scan, oldest first."""
    dirt_streak = 0

    for frame in frames:
        has_dirt = any(box.cls == "dirt" and box.conf >= dirt_conf for box in frame)
        if has_dirt:
            dirt_streak += 1
            if dirt_streak >= dirt_min_frames:
                return "dirt"
        else:
            dirt_streak = 0
    return "clean"