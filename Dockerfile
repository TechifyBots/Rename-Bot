FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=Asia/Kolkata

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    tzdata \
    curl gnupg ca-certificates \
    && curl -fsSL https://packagecloud.io/ookla/speedtest-cli/gpgkey | gpg --dearmor -o /usr/share/keyrings/ookla-speedtest.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/ookla-speedtest.gpg] https://packagecloud.io/ookla/speedtest-cli/debian/ bookworm main" > /etc/apt/sources.list.d/ookla.list \
    && apt-get update && apt-get install -y --no-install-recommends speedtest \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]