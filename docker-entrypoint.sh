#!/bin/sh
# /srv/portfolio/docker-entrypoint.sh
# ---

# Wait for Postgres
while ! nc -z db 5432; do
  echo "Waiting for Postgres..."
  sleep 1
done

# --- ADD THIS SECTION ---
# This script is run as root, so we can fix permissions
# on the volumes mounted by docker-compose.
echo "Setting ownership for mounted volumes..."
chown -R app:app /app/mediafiles
chown -R app:app /app/staticfiles
# --- END ADDED SECTION ---

# --- MODIFIED LINES ---
# Use 'gosu' to run the following commands as the 'app' user
echo "Applying database migrations as 'app' user..."
gosu app python manage.py migrate --noinput

echo "Collecting static files as 'app' user..."
gosu app python manage.py collectstatic --noinput

echo "Starting Gunicorn server as 'app' user..."
# Use 'exec' to replace this script with the gunicorn process
exec gosu app gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:8000
# --- END MODIFIED LINES ---