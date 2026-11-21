"""WebSocket /ws text messages. Contract: systems/api.md. Binary messages are display JPEGs."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


# frontend -> backend
class UvSet(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["uv_set"]
    channel: int = Field(ge=0, le=2)  # index into uv_gpio
    on: bool


class ScanStart(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["scan_start"]


class BinaryView(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["binary_view"]
    on: bool


ClientMessage = Annotated[UvSet | ScanStart | BinaryView, Field(discriminator="type")]


# backend -> frontend
class UvState(BaseModel):
    type: Literal["uv"] = "uv"
    channels: list[bool]


class ScanState(BaseModel):
    """Sent about every 0.5 seconds while scanning, and once when done."""

    type: Literal["scan"] = "scan"
    state: Literal["idle", "scanning", "done"]
    remaining_s: float | None  # seconds left while scanning, else null
    result: Literal["clean", "dirt"] | None  # set when state == "done"


class Error(BaseModel):
    type: Literal["error"] = "error"
    message: str
