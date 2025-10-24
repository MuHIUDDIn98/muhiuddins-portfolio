#!/bin/sh
# /srv/portfolio/docker-entrypoint.sh
# ---

# --- UNCOMMENT THESE LINES ---
while ! nc -z db 5432; do
  echo "Waiting for Postgres..."
  sleep 1
done
# -----------------------------

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:8000