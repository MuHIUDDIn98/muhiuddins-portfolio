# /srv/portfolio/Dockerfile
# ---

# --- Stage 1: The Builder ---
# This stage installs dependencies
FROM python:3.10-slim-bullseye AS builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install pip and system dependencies
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev

# Copy and install requirements
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt


# --- Stage 2: The Runtime ---
# This stage builds the final, lean image
FROM python:3.10-slim-bullseye

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Install production system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-traditional && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

# Copy installed packages from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Set work directory
WORKDIR /app

# --- UPDATED SECTION ---
# 1. Copy the entire project first
COPY . .

# 2. NOW, set the execute permission on the script
RUN chmod +x /app/docker-entrypoint.sh
# --- END UPDATE ---

# Change ownership to the non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# This entrypoint script will run migrations and start gunicorn
ENTRYPOINT ["/app/docker-entrypoint.sh"]