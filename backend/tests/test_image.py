import numpy as np
import simplejpeg

from app.utils.image import COLORS, Box, draw_boxes, render_frame


def test_render_frame_crops_and_draws_box() -> None:
    src = simplejpeg.encode_jpeg(np.full((100, 200, 3), 128, np.uint8), quality=95)
    box = [Box("dirt", 0.9, 0, 0, 1, 1)]

    img = simplejpeg.decode_jpeg(render_frame(src, (0, 0, 0.5, 1), 100, box, 95))
    assert img.shape[:2] == (100, 100)  # left half at full scale: 100 / 0.5 needs the whole 200 px
    r, g, _ = img[50, 1]
    assert r > 200 and g < 80  # red dirt box on the left edge
    assert abs(int(img[50, 50, 0]) - 128) < 10  # inside untouched

    img = simplejpeg.decode_jpeg(render_frame(src, (0, 0, 0.5, 1), 50, box, 95))
    assert img.shape[:2] == (50, 50)  # 1/2-scale decode is already wide enough


def test_draw_boxes_clamps_and_accepts_swapped_corners() -> None:
    img = np.zeros((10, 10, 3), np.uint8)
    draw_boxes(img, [Box("hand", 1.0, 1.5, 1.2, 0.5, 0.5)], thickness=1)  # x1 > x2, past the edge
    assert tuple(img[5, 5]) == COLORS["hand"]  # top-left corner at (0.5, 0.5)
    assert tuple(img[9, 9]) == COLORS["hand"]  # clamped to the last pixel
    assert tuple(img[0, 0]) == (0, 0, 0)  # outside the box untouched
