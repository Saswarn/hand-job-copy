from app.services.scan import judge
from app.utils.image import Box


hand = Box("hand", 0.9, 0.1, 0.1, 0.2, 0.2)
dirt = Box("dirt", 0.9, 0.1, 0.1, 0.2, 0.2)
dirt_below = Box("dirt", 0.49, 0.1, 0.1, 0.2, 0.2)
dirt_at_threshold = Box("dirt", 0.5, 0.1, 0.1, 0.2, 0.2)


def test_judge_no_frame() -> None:
    result = judge([], dirt_conf = 0.5, dirt_min_frames = 3)
    assert result == "clean"


def test_judge_all_frames_only_hand() -> None:
    result = judge([[hand], [hand], [hand]], dirt_conf = 0.5, dirt_min_frames = 3)
    assert result == "clean"


def test_dirt_3_frames_in_a_row() -> None:
    frames = [[dirt], [dirt], [dirt]]
    result = judge(frames, dirt_conf = 0.5, dirt_min_frames = 3)
    assert result == "dirt"


def test_dirt_2_frames_in_a_row() -> None:
    frames = [[dirt], [dirt], [hand]]
    result = judge(frames, dirt_conf = 0.5, dirt_min_frames = 3)
    assert result == "clean"


def test_dirt_2_frames_1_no_frames_2_dirt_frames() -> None:
    frames = [[dirt], [dirt], [], [dirt], [dirt]]
    result = judge(frames, dirt_conf = 0.5, dirt_min_frames = 3)
    assert result == "clean"


def test_dirt_conf_below_condition_3_frames() -> None:
    frames = [[dirt_below], [ dirt_below], [dirt_below]]
    result = judge(frames, dirt_conf = 0.5, dirt_min_frames = 3)
    assert result == "clean"


def test_dirt_conf_at_condition_3_frames() -> None:
    frames = [[dirt_at_threshold], [dirt_at_threshold], [dirt_at_threshold]]
    result = judge(frames, dirt_conf = 0.5, dirt_min_frames = 3)
    assert result == "dirt"