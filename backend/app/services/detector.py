from app.utils.image import Box, Image


class Detector:
    """AI hook, not implemented yet: Stream draws whatever latest() returns on every display frame.

    TODO(AI): load the .onnx from backend/models/ once, run detect() on frames in its own thread
    (5-10 fps on the Pi) and keep the newest result for latest(). Spec: systems/spec/ai.md
    """

    def detect(self, image: Image) -> list[Box]:
        """RGB image cropped like the display frame -> boxes, coordinates 0-1 of that image.

        Preprocess must match training: binary -> letterbox 640.
        """
        return []

    def latest(self) -> list[Box]:
        """Newest boxes. Called by the stream thread for every frame, so it must not block."""
        return []
