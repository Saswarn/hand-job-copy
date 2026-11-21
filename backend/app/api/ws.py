import asyncio
import contextlib
import logging
import time

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import TypeAdapter, ValidationError

from app.core.config import AppConfig
from app.schemas.ws import ClientMessage, Error, ScanStart, ScanState, UvSet, UvState
from app.services.detector import Detector
from app.services.scan import judge
from app.services.stream import Stream
from app.services.uv import UvService
from app.utils.image import Box


router = APIRouter()
log = logging.getLogger(__name__)
_client_message: TypeAdapter[ClientMessage] = TypeAdapter(ClientMessage)


@router.websocket("/ws")
async def ws(websocket: WebSocket) -> None:
    uv: UvService = websocket.app.state.uv
    stream: Stream = websocket.app.state.stream
    detector: Detector = websocket.app.state.detector
    await websocket.accept()
    frames = asyncio.create_task(_send_frames(websocket, stream))
    scan_task: asyncio.Task[None] | None = None
    try:
        await websocket.send_text(UvState(channels=uv.state()).model_dump_json())
        while True:
            raw = await websocket.receive_text()
            try:
                msg = _client_message.validate_json(raw)
            except ValidationError as e:
                await websocket.send_text(Error(message=str(e)).model_dump_json())
                continue
            if isinstance(msg, UvSet):
                uv.set(msg.channel, msg.on)
                await websocket.send_text(UvState(channels=uv.state()).model_dump_json())
            elif isinstance(msg, ScanStart):
                if scan_task is not None and not scan_task.done():
                    await websocket.send_text(Error(message="scan already in progress").model_dump_json())
                    continue
                else:
                    cfg: AppConfig = websocket.app.state.config
                    scan_task = asyncio.create_task(_scan(websocket, uv, detector, cfg))
            else:
                # TODO(backend): binary_view -> stream the binary image the AI sees instead of the display frame
                await websocket.send_text(Error(message=f"{msg.type} is not implemented yet").model_dump_json())
    except WebSocketDisconnect:
        pass
    finally:
        uv.all_off()  # frontend gone -> every UV channel off (systems/api.md)
        try:
            if scan_task is not None:
                scan_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await scan_task
        finally:
            frames.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await frames


async def _send_frames(websocket: WebSocket, stream: Stream) -> None:
    """Send only the newest display frame; a slow client skips frames instead of queueing them."""
    seq = 0
    with contextlib.suppress(WebSocketDisconnect, RuntimeError):  # socket closed under us
        while True:
            seq, jpeg = await asyncio.to_thread(stream.latest.wait_newer, seq, 0.5)
            if jpeg is not None:
                await websocket.send_bytes(jpeg)


async def _scan(websocket: WebSocket, uv: UvService, detector: Detector, cfg: AppConfig) -> None:
    try:
        for i in range(3):
            uv.set(i, True)
        end_time = time.monotonic() + cfg.scan_seconds
        await websocket.send_text(UvState(channels=uv.state()).model_dump_json())
        ai_frames: list[list[Box]] = []
        while time.monotonic() < end_time:
            ai_frames.append(list(detector.latest()))
            time_left = max(0.0, end_time - time.monotonic())
            await websocket.send_text(
                ScanState(state="scanning", remaining_s=time_left, result=None).model_dump_json()
            )
            await asyncio.sleep(min(0.5, max(0.0, end_time - time.monotonic())))
        result = judge(ai_frames, cfg.dirt_conf, cfg.dirt_min_frames)
        uv.all_off()  # done must never report completion while the lights are still on
        await websocket.send_text(ScanState(state="done", remaining_s=None, result=result).model_dump_json())
    except WebSocketDisconnect:
        pass
    except Exception:
        log.exception("scan failed")
        uv.all_off()
        with contextlib.suppress(WebSocketDisconnect, RuntimeError):
            await websocket.send_text(Error(message="scan failed").model_dump_json())
    finally:
        uv.all_off()
        try:
            await websocket.send_text(UvState(channels=uv.state()).model_dump_json())
        except (WebSocketDisconnect, RuntimeError):
            pass
