# Minimal stubs for simplejpeg (ships no types). Only the arguments this project passes.
import numpy as np
import numpy.typing as npt

def decode_jpeg(
    data: bytes,
    colorspace: str = "rgb",
    fastdct: bool = False,
    fastupsample: bool = False,
    min_height: int = 0,
    min_width: int = 0,
) -> npt.NDArray[np.uint8]: ...
def encode_jpeg(
    image: npt.NDArray[np.uint8],
    quality: int = 85,
    colorspace: str = "rgb",
    colorsubsampling: str = "444",
    fastdct: bool = True,
) -> bytes: ...
