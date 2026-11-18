#!/bin/sh
set -e

echo "=== [Library.io Backend Initialization] ==="

# 1. Wait for PostgreSQL Database
if [ "$DB_ENGINE" = "django.db.backends.postgresql" ] || [ -n "$DB_HOST" ]; then
    echo "Waiting for PostgreSQL at $DB_HOST:${DB_PORT:-5432}..."
    while ! nc -z "$DB_HOST" "${DB_PORT:-5432}"; do
        sleep 0.5
    done
    echo "[OK] PostgreSQL is reachable."
fi

# 2. Run Database Migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# 3. Collect Static Files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

# 4. Optional Seed & Elasticsearch Indexing
if [ "$SEED_ON_STARTUP" = "true" ] || [ "$SEED_ON_STARTUP" = "1" ]; then
    echo "Seeding default catalog and user accounts..."
    python manage.py seed_library || true
fi

if [ "$INDEX_ON_STARTUP" = "true" ] || [ "$INDEX_ON_STARTUP" = "1" ]; then
    echo "Checking Elasticsearch index..."
    python manage.py index_books || true
fi

echo "=== [Backend Initialization Complete — Launching WSGI Server] ==="
exec "$@"
