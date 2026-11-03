import asyncio
import contextlib

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import TypeAdapter, ValidationError

from app.schemas.ws import ClientMessage, Error, UvSet, UvState
from app.services.stream import Stream
from app.services.uv import UvService

router = APIRouter()
_client_message: TypeAdapter[ClientMessage] = TypeAdapter(ClientMessage)


@router.websocket("/ws")
async def ws(websocket: WebSocket) -> None:
    uv: UvService = websocket.app.state.uv
    stream: Stream = websocket.app.state.stream
    await websocket.accept()
    frames = asyncio.create_task(_send_frames(websocket, stream))
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
            else:
                # TODO(backend): scan_start -> UV on, scan for scan_seconds, send ScanState, UV off in finally
                # TODO(backend): binary_view -> stream the binary image the AI sees instead of the display frame
                await websocket.send_text(Error(message=f"{msg.type} is not implemented yet").model_dump_json())
    except WebSocketDisconnect:
        pass
    finally:
        uv.all_off()  # frontend gone -> every UV channel off (systems/api.md)
        frames.cancel()


async def _send_frames(websocket: WebSocket, stream: Stream) -> None:
    """Send only the newest display frame; a slow client skips frames instead of queueing them."""
    seq = 0
    with contextlib.suppress(WebSocketDisconnect, RuntimeError):  # socket closed under us
        while True:
            seq, jpeg = await asyncio.to_thread(stream.latest.wait_newer, seq, 0.5)
            if jpeg is not None:
                await websocket.send_bytes(jpeg)
