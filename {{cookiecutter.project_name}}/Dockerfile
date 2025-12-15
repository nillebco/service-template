FROM python:3.12-slim AS builder

ARG PORT=17581

WORKDIR /app

# Copy uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get clean && \
    apt-get -y update && \
    apt-get install -y --no-install-recommends \
    cmake \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    addgroup --system appuser && \
    adduser --system appuser --disabled-login && \
    chown -R appuser:appuser /app

COPY pyproject.toml uv.lock ./
COPY api/ ./api/
COPY static/ ./static/

USER appuser

RUN cd /app && \
    uv sync --frozen --no-cache && \
    mkdir data secrets

FROM python:3.12-slim AS runner
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    pandoc && \
    apt-get clean && \
    addgroup --system appuser && \
    adduser --system appuser --disabled-login \
    --ingroup appuser --no-create-home \
    --home /nonexistent --gecos "nonroot user" --shell /bin/false || true

COPY --from=builder /app/ /app/
RUN chown -R appuser:appuser /app/data /app/secrets
USER appuser

WORKDIR /app
VOLUME [ "/app/data", "/app/secrets" ]
ENV NUMBA_CACHE_DIR=/app/data
ENV PORT=$PORT
EXPOSE $PORT
CMD ["/bin/sh", "-c", ".venv/bin/uvicorn api.app:app --host 0.0.0.0 --port $PORT"]
