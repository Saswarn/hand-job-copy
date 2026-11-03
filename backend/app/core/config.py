import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.json"


# ponytail: plain dict for now; HAN-10 replaces this with a Pydantic model + GET/PUT /config.
def load_config(path: Path = CONFIG_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
