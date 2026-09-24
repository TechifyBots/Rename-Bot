# ---------- builder: resolve + build wheels (dropped, never shipped) ----------
FROM python:3.14-slim AS builder

ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /wheels

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip wheel --wheel-dir /wheels -r requirements.txt


# ---------- runtime: minimal deploy image ----------
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=Asia/Kolkata

# Runtime-only apt deps. curl/gnupg exist for one RUN only (Ookla repo
# setup) then purged so they don't bloat the final layer.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        tzdata \
        ca-certificates \
        curl \
        gnupg \
    && curl -fsSL https://packagecloud.io/ookla/speedtest-cli/gpgkey | gpg --dearmor -o /usr/share/keyrings/ookla-speedtest.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/ookla-speedtest.gpg] https://packagecloud.io/ookla/speedtest-cli/debian/ bookworm main" > /etc/apt/sources.list.d/ookla.list \
    && apt-get update && apt-get install -y --no-install-recommends speedtest \
    && apt-get purge -y curl gnupg \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --upgrade pip && \
    pip install --no-cache-dir /wheels/*.whl && \
    rm -rf /wheels

COPY . .

# Pre-compile bytecode so cold start skips recompilation (compileall writes
# explicitly even with PYTHONDONTWRITEBYTECODE=1).
RUN python -m compileall -q bot.py config.py helper plugins

CMD ["python", "bot.py"]
