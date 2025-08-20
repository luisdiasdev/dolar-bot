# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.13-slim-bookworm@sha256:9b8102b7b3a61db24fe58f335b526173e5aeaaf7d

RUN groupadd --gid 5678 appgroup && \
    useradd --uid 5678 --gid appgroup --shell /bin/bash --create-home appuser

# Security: Update system packages and remove package cache
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Security: Disable pip cache and use security flags  
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Create app directory with proper permissions
RUN mkdir -p /app && chown -R appuser:appgroup /app

# Switch to non-root user early
USER appuser

# Sets workdir
WORKDIR /app

# Copy requirements first for better layer caching
COPY --chown=appuser:appgroup requirements.txt .

# Install pip requirements with security flags
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appgroup . .

# Security: Remove write permissions from application files
RUN find /app -name "*.py" -exec chmod 644 {} \; && \
    find /app -type d -exec chmod 755 {} \; && \
    chmod 644 /app/main.py

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "-u", "-m", "main"]
