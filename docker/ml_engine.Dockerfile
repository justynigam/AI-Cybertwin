# Stage 1: Builder (Heavy, contains compilers)
FROM python:3.12-slim AS builder

WORKDIR /app
# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc

# Install python dependencies into a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY synthetic_data/requirements.txt .
# Install PyTorch CPU version (Massive space saver for inference)
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Stage 2: Production (Lightweight, no compilers)
FROM python:3.12-slim

WORKDIR /app
# Copy the compiled virtual environment from Stage 1
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code and model weights
COPY behavior_twin/ /app/behavior_twin/
COPY ml/ /app/ml/

# Run as a non-root user (CRITICAL Security Best Practice)
RUN useradd -m cybertwin_user
USER cybertwin_user

# Command to start the Redis consumer/inference worker
CMD ["python", "-m", "backend.app.workers.inference_worker"]
