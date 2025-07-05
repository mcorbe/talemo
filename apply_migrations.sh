#!/bin/bash

# Exit on error
set -e

echo "Applying migrations for shared apps (public schema)..."
python manage.py migrate_schemas --shared

echo "Applying migrations for all tenants..."
python manage.py migrate_schemas

echo "Migrations applied successfully!"