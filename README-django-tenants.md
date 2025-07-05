# Django Tenants Setup

This document provides instructions for setting up and initializing the multi-tenant functionality in the Talemo project.

## Initial Setup

Follow these steps to set up the multi-tenant functionality:

1. Run migrations for shared apps (public schema):

```bash
python manage.py migrate_schemas --shared
```

2. Initialize the public tenant:

```bash
python manage.py init_public_tenant --domain=localhost --username=admin --password=yourpassword --email=admin@example.com
```

3. Run migrations for all tenants:

```bash
python manage.py migrate_schemas
```

## Creating Additional Tenants

You can create additional tenants programmatically:

```python
from django.contrib.auth.models import User
from talemo.core.models import Tenant, Domain

# Get or create a user to be the owner
user = User.objects.get(username='admin')

# Create tenant
tenant = Tenant(schema_name='tenant1', name='Tenant 1', owner=user)
tenant.save()

# Create domain for tenant
domain = Domain(domain='tenant1.localhost', tenant=tenant, is_primary=True)
domain.save()
```

## Troubleshooting

If you encounter the error `relation "core_tenant" does not exist`, it means you need to run the migrations for the shared apps first:

```bash
python manage.py migrate_schemas --shared
```

Then initialize the public tenant and run migrations for all tenants.