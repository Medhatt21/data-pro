#!/bin/bash
set -e

echo "Waiting for database to be ready..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "Database is ready!"

echo "Initializing Superset database..."
superset db upgrade

echo "Creating admin user..."
superset fab create-admin \
    --username ${SUPERSET_ADMIN_USERNAME} \
    --firstname Admin \
    --lastname User \
    --email ${SUPERSET_ADMIN_EMAIL} \
    --password ${SUPERSET_ADMIN_PASSWORD} || echo "Admin user already exists"

echo "Loading examples..."
superset load_examples || echo "Examples already loaded"

echo "Initializing roles and permissions..."
superset init

echo "Starting Superset..."
exec superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger 