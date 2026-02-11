# Wukong Defense Framework: Universal Proxy
# Multi-stage build for a lightweight image

FROM python:3.10-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy local package files
COPY pyproject.toml .
COPY README.md .
COPY src/ /app/src/

# Install the package and production server
RUN pip install --no-cache-dir . uvicorn gunicorn

# Default environment variables
ENV TARGET_URL="http://localhost:8080"
ENV HOST="0.0.0.0"
ENV PORT="8000"

# Expose Wukong Proxy Port
EXPOSE 8000

# Entrypoint: Run Wukong Proxy
CMD ["sh", "-c", "uvicorn wukong.proxy:app --host $HOST --port $PORT"]
