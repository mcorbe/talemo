#!/bin/bash

# Exit on error
set -e

echo "Setting up multi-tenant functionality..."

# Run migrations for shared apps (public schema)
echo "Running migrations for shared apps..."
python manage.py migrate_schemas --shared

# Seed the database with initial data
echo "Seeding the database with initial data..."
python manage.py seed_data --domain=localhost --admin-username=admin --admin-password=admin --admin-email=admin@example.com --create-test-users

# Run migrations for all tenants
echo "Running migrations for all tenants..."
python manage.py migrate_schemas

echo "Multi-tenant setup complete!"
