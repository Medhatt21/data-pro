FROM apache/superset:latest

# Switch to root to install additional packages
USER root

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install additional Python packages
RUN pip install --no-cache-dir \
    psycopg2-binary \
    redis \
    celery \
    flask-cors

# Switch back to superset user
USER superset

# Copy configuration file
COPY superset_config.py /app/superset_config.py

# Set environment variables
ENV SUPERSET_CONFIG_PATH=/app/superset_config.py
ENV FLASK_APP=superset

# Initialize the database and create admin user
COPY init_superset.sh /app/init_superset.sh
USER root
RUN chmod +x /app/init_superset.sh
USER superset

# Expose port
EXPOSE 8088

# Start superset
CMD ["/app/init_superset.sh"] 