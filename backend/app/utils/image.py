import math
from typing import Literal, NamedTuple

import numpy as np
import simplejpeg


class Box(NamedTuple):
    """Detection box, coordinates 0-1 relative to the cropped image."""

    cls: Literal["hand", "dirt"]
    conf: float
    x1: float
    y1: float
    x2: float
    y2: float


COLORS = {"hand": (0, 200, 0), "dirt": (255, 0, 0)}


def render_frame(jpeg: bytes, crop: list[float], min_width: int, boxes: list[Box], quality: int) -> bytes:
    """Camera JPEG -> display JPEG: scaled decode -> crop [x1, y1, x2, y2] (0-1) -> draw boxes -> encode.

    Decodes at the smallest 1/n scale whose crop is still >= min_width wide, so the output
    is between min_width and 2x min_width (or the full crop if the camera is smaller).
    """
    x1, y1, x2, y2 = crop
    img = simplejpeg.decode_jpeg(
        jpeg, min_width=math.ceil(min_width / (x2 - x1)), fastdct=True, fastupsample=True
    )
    h, w, _ = img.shape
    img = img[round(y1 * h) : round(y2 * h), round(x1 * w) : round(x2 * w)]
    draw_boxes(img, boxes)
    return simplejpeg.encode_jpeg(np.ascontiguousarray(img), quality=quality)


def draw_boxes(img: np.ndarray, boxes: list[Box], thickness: int = 3) -> None:
    h, w, _ = img.shape
    for b in boxes:
        left, right = sorted(min(max(round(v * w), 0), w) for v in (b.x1, b.x2))
        top, bottom = sorted(min(max(round(v * h), 0), h) for v in (b.y1, b.y2))
        color = COLORS[b.cls]
        img[top : top + thickness, left:right] = color
        img[max(bottom - thickness, top) : bottom, left:right] = color
        img[top:bottom, left : left + thickness] = color
        img[top:bottom, max(right - thickness, left) : right] = color
