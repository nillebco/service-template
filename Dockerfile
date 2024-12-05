FROM python:3-slim as builder

ARG PORT 17581
WORKDIR /app

COPY api/ ./api/
COPY requirements.txt ./
COPY static/ ./static/

RUN apt-get clean && \
    apt-get -y update && \
    apt-get install -y --no-install-recommends \
    cmake \
    build-essential && \
    apt-get clean && \
    pip install --upgrade pip

RUN cd /app && \
    pip install uv && \
    uv venv && \
    . .venv/bin/activate && \
    uv pip install --no-cache-dir -r requirements.txt && \
    pip cache purge && \
    uv cache clean && \
    mkdir data secrets

FROM python:3-slim as runner
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
EXPOSE $PORT
CMD [".venv/bin/uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", $PORT]