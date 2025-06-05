FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Create pyproject.toml for dependencies
COPY pyproject.toml ./

# Install Python packages using uv
RUN uv pip install --system -r pyproject.toml

# Create lab_root directory
RUN mkdir -p /app/lab_root

# Expose port
EXPOSE 8888

# Start marimo server
CMD ["marimo", "edit", "--host", "0.0.0.0", "--port", "8888", "--no-token", "/app/lab_root"] 