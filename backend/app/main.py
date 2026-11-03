import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import config, health, ws
from app.core.config import load_config
from app.services.camera import Camera, open_camera
from app.services.detector import Detector
from app.services.stream import Stream
from app.services.uv import UvService

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.config = cfg = load_config()
    app.state.uv = uv = UvService(cfg.uv_gpio)  # every channel starts off
    camera: Camera | None = None
    stream: Stream | None = None
    try:
        camera = open_camera(cfg.camera)
        app.state.stream = stream = Stream(camera, Detector(), cfg.camera.crop, cfg.stream)
        camera.start()
        stream.start()
        yield
    finally:
        uv.close()  # UV off before anything else
        for service in (stream, camera):
            if service:
                service.stop()


app = FastAPI(title="HandCleanStation", lifespan=lifespan)
# Electron renderer: http://localhost:<vite port> in dev, file:// ("null" origin) when packaged.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(health.router)
app.include_router(config.router)
app.include_router(ws.router)


@app.exception_handler(Exception)
async def on_error(request: Request, exc: Exception) -> JSONResponse:
    request.app.state.uv.all_off()
    log.exception("unhandled error", exc_info=exc)
    return JSONResponse({"detail": "internal error"}, status_code=500)
