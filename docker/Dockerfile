FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY main.py .
COPY duplocloud_mcp/ duplocloud_mcp/

RUN uv sync --frozen --no-dev --no-editable

FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --no-create-home appuser

WORKDIR /app
COPY --from=builder /app /app

USER appuser

ENTRYPOINT ["uv", "run", "python", "main.py"]
