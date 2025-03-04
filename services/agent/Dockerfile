# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM python:3.12-alpine AS app

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app
WORKDIR /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
ENV DRONETAG_AGENT_CONFIG_FILE="/data/config.json"
ENV UVICORN_NO_ACCESS_LOG=1
ENV MAVLINK_ENDPOINT_IP="172.17.0.1" MAVLINK_ENDPOINT_PORT=5790

# Launch FastAPI application
CMD ["fastapi", "run", "main.py", "--root-path", "/apps/com.starcopter.dronetag-agent"]
