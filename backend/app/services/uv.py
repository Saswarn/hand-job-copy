from gpiozero import OutputDevice


class UvService:
    """UV light channels. Pin factory comes from GPIOZERO_PIN_FACTORY (mock on dev, lgpio on Pi)."""

    def __init__(self, pins: list[int]):
        # Relay polarity is not confirmed yet (systems/hardware.md Open items): active-high for now.
        # initial_value=False -> every channel starts off.
        self._channels = [OutputDevice(pin, active_high=True, initial_value=False) for pin in pins]

    def set(self, channel: int, on: bool) -> None:
        self._channels[channel].value = on

    def all_off(self) -> None:
        for ch in self._channels:
            ch.off()

    def state(self) -> list[bool]:
        return [bool(ch.value) for ch in self._channels]

    def close(self) -> None:
        self.all_off()
        for ch in self._channels:
            ch.close()
