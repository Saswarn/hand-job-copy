# Matches Raspberry Pi 5 / Raspberry Pi OS Bookworm (Debian 12, arm64). Build with --platform linux/arm64.
FROM ghcr.io/astral-sh/uv:0.11.8 AS uv

FROM python:3.11.15-slim-bookworm
COPY --from=uv /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH=/opt/venv/bin:$PATH

WORKDIR /app
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-dev --no-install-project

COPY app ./app
COPY config.json ./

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
