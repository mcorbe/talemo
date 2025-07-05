#!/bin/bash

# Exit on error
set -e

echo "Setting up multi-tenant functionality..."

# Run migrations for shared apps (public schema)
echo "Running migrations for shared apps..."
python manage.py migrate_schemas --shared

# Initialize the public tenant
echo "Initializing public tenant..."
python manage.py init_public_tenant --domain=localhost --username=admin --password=admin --email=admin@example.com

# Run migrations for all tenants
echo "Running migrations for all tenants..."
python manage.py migrate_schemas

echo "Multi-tenant setup complete!"