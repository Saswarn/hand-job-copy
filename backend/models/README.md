# models/

Put the ONNX model here. Model files are not in git (distribute them separately); only this README and `.gitkeep` are tracked.

| File | Used by | Notes |
|---|---|---|
| `*.onnx` | `app/services` AI detector (not wired yet, see `systems/spec/ai.md`) | input: binary image, letterbox 640×640 · classes `hand`, `dirt` |

Docker mounts this folder at `/app/models` (`docker-compose.yml`).
