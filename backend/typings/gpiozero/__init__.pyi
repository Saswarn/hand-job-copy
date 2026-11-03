# Minimal stubs for the gpiozero API this project uses (gpiozero ships no types).
# Add a name here before using it in app/ or tests/.

class Pin:
    @property
    def state(self) -> float: ...

class Factory:
    def pin(self, spec: int) -> Pin: ...

class Device:
    pin_factory: Factory | None
    def close(self) -> None: ...

class OutputDevice(Device):
    def __init__(
        self,
        pin: int,
        *,
        active_high: bool = True,
        initial_value: bool | None = False,
        pin_factory: Factory | None = None,
    ) -> None: ...
    @property
    def value(self) -> int: ...
    @value.setter
    def value(self, value: bool) -> None: ...
    def on(self) -> None: ...
    def off(self) -> None: ...
