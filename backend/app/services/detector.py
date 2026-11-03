from app.utils.image import Box

MOCK_BOXES = [
    Box("hand", 0.9, 0.25, 0.2, 0.75, 0.9),
    Box("dirt", 0.7, 0.45, 0.45, 0.55, 0.55),
]


class MockDetector:
    """Stand-in until the ONNX model lands. The real detector runs in its own thread
    and exposes its newest result through latest() the same way."""

    def latest(self) -> list[Box]:
        return MOCK_BOXES
