from fastapi import FastAPI

# Routes, /ws and services (camera, ai, uv) go in app/api and app/services.
# Contract: systems/api.md
app = FastAPI(title="HandCleanStation")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
