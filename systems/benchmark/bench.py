"""Pipeline benchmark — run on the real Pi 5 (numbers from Windows/QEMU are meaningless).

    uv run --project backend python systems/benchmark/bench.py

Fill each TODO, then record results in systems/metrics/{backend,ai,hardware}.md.
"""

import time
from collections.abc import Callable

N = 100  # frames per stage


def bench(name: str, fn: Callable[[], object], n: int = N) -> None:
    fn()  # warm-up
    t = time.perf_counter()
    for _ in range(n):
        fn()
    ms = (time.perf_counter() - t) / n * 1000
    print(f"{name:<10} {ms:8.2f} ms/frame  {1000 / ms:7.1f} fps")


def grab() -> bytes:
    # TODO: one raw MJPEG frame from /dev/video0 via linuxpy at config.camera.capture
    raise NotImplementedError


def decode(jpeg: bytes):
    # TODO: simplejpeg.decode_jpeg(jpeg, colorspace="GRAY", min_height=..., min_width=...)
    raise NotImplementedError


def binary(img):
    # TODO: crop (config.camera.crop) + threshold (config.binary_threshold) + letterbox 640x640
    raise NotImplementedError


def infer(x):
    # TODO: onnxruntime session on backend/models/<model>.onnx
    raise NotImplementedError


if __name__ == "__main__":
    for name, fn in [("grab", grab), ("decode", decode), ("binary", binary), ("infer", infer)]:
        print(f"{name:<10} TODO")
    # Once implemented:
    # jpeg = grab(); bench("grab", grab)
    # img = decode(jpeg); bench("decode", lambda: decode(jpeg))
    # x = binary(img); bench("binary", lambda: binary(img))
    # bench("infer", lambda: infer(x))
    # bench("total", lambda: infer(binary(decode(grab()))))
