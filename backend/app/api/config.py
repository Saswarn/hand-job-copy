from pathlib import Path

from fastapi import APIRouter, Request

from app.core.config import AppConfig, save_config

router = APIRouter()


@router.get("/config")
def get_config(request: Request) -> AppConfig:
    config: AppConfig = request.app.state.config
    return config


@router.put("/config", status_code=204)
def put_config(new: AppConfig, request: Request) -> None:
    """Save validated config before updating the in-memory state."""
    config_path: Path = request.app.state.config_path
    save_config(new, config_path)
    request.app.state.config = new
