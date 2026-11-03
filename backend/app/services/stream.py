import logging
import threading

from app.services.camera import Camera
from app.services.detector import Detector
from app.services.latest import Latest
from app.utils.image import render_frame

log = logging.getLogger(__name__)


class Stream:
    """Display frames in their own thread: always renders the newest camera frame, skips the rest."""

    def __init__(self, camera: Camera, detector: Detector, crop: list[float], min_width: int, quality: int):
        self.latest: Latest[bytes] = Latest()
        self._camera = camera
        self._detector = detector
        self._crop = crop
        self._min_width = min_width
        self._quality = quality
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, name="stream", daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join(timeout=2)

    def _run(self) -> None:
        seq = 0
        while not self._stop.is_set():
            seq, jpeg = self._camera.latest.wait_newer(seq, timeout=0.5)
            if jpeg is None:
                continue
            try:
                frame = render_frame(jpeg, self._crop, self._min_width, self._detector.latest(), self._quality)
            except Exception:
                log.exception("render failed, frame skipped")  # e.g. a corrupt JPEG from the camera
                continue
            self.latest.put(frame)
