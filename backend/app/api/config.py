from fastapi import APIRouter, HTTPException, Request

from app.core.config import AppConfig

router = APIRouter()


@router.get("/config")
def get_config(request: Request) -> AppConfig:
    config: AppConfig = request.app.state.config
    return config


@router.put("/config", status_code=204)
def put_config(new: AppConfig) -> None:
    """Body is validated against AppConfig (bad values -> 422) before this runs.

    TODO(backend): write config.json atomically (temp file + os.replace), swap app.state.config,
    and apply what can change live (camera controls, stream, scan params). Contract: systems/api.md
    """
    raise HTTPException(status_code=501, detail="PUT /config is not implemented yet")
