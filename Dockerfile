# Stage 1: Build Image
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies required for building wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements mapping
COPY requirements.txt .

# Install dependencies into wheelhouse to simply copy them
# Also installing gunicorn as it is required to run the production server
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt gunicorn

# Stage 2: Final Runtime Image
FROM python:3.11-slim

WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder and install them
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy application files
COPY . .

# Non-root user — never run production containers as root
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Base command for API, Celery worker command will be overridden in docker-compose
CMD ["gunicorn", "main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "60", \
     "--graceful-timeout", "30"]
