#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "=== [Render Build Step: Python Dependencies] ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== [Render Build Step: Collect Static Files] ==="
python manage.py collectstatic --no-input

echo "=== [Render Build Step: Database Migrations] ==="
python manage.py migrate

echo "=== [Render Build Step: Production Seeding] ==="
python manage.py seed_production

echo "=== [Render Build Complete] ==="
