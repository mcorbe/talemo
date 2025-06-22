# Core Module

This module provides fundamental functionality used throughout the application, including multi-tenant infrastructure, user authentication and profiles, permissions and access control, and common utilities and middleware.

## Models

- **Tenant**
  - `id`: UUID (PK)
  - `name`: CharField
  - `type`: CharField [family, institution]
  - `created_at`: DateTimeField
  - `updated_at`: DateTimeField

- **Profile**
  - `id`: UUID (PK)
  - `tenant_id`: ForeignKey(Tenant)
  - `name`: CharField (unique within tenant)
  - `permissions`: JSONField
  - `created_at`: DateTimeField
  - `updated_at`: DateTimeField

- **User**
  - `id`: UUID (PK)
  - `tenant_id`: ForeignKey(Tenant)
  - `profile_id`: ForeignKey(Profile)
  - `email`: EmailField
  - `name`: CharField
  - `is_active`: BooleanField
  - `created_at`: DateTimeField
  - `last_login`: DateTimeField

- **UserIdentity**
  - `id`: UUID (PK)
  - `user_id`: ForeignKey(User)
  - `idp_issuer`: CharField
  - `idp_subject`: CharField
  - `created_at`: DateTimeField
  - `metadata`: JSONField

- **TenantPolicy**
  - `id`: UUID (PK)
  - `tenant_id`: ForeignKey(Tenant)
  - `key`: CharField (unique within tenant)
  - `value`: JSONField
  - `created_at`: DateTimeField
  - `updated_at`: DateTimeField

## URLs

- `/api/auth/google/` - Google SSO authentication
- `/api/auth/apple/` - Apple Sign-In authentication
- `/api/auth/token/` - Get JWT token
- `/api/auth/token/refresh/` - Refresh JWT token
- `/api/tenants/` - Get current tenant details
- `/api/tenants/policies/` - Get tenant policies
- `/api/tenants/policies/<key>/` - Update tenant policy (Admin)
- `/api/profiles/` - List profiles in current tenant
- `/api/profiles/` - Create new profile (Admin)
- `/api/profiles/<id>/` - Get profile details
- `/api/profiles/<id>/` - Update profile (Admin)
- `/api/profiles/<id>/` - Delete profile (Admin)
- `/api/profiles/<id>/assign/` - Assign users to profile (Admin)
- `/api/admin/stats/` - Get platform statistics
- `/api/admin/users/` - List users (Admin)
- `/api/admin/users/<id>/` - Update user (Admin)
- `/api/admin/audit-logs/` - Get audit logs (Admin)

## Views

- Authentication views for Google and Apple SSO
- JWT token views
- Tenant management views
- Profile management views
- Admin dashboard views
- User management views
- Audit log views

## API Endpoints

### Authentication
- `POST /api/auth/google/` - Google SSO authentication
- `POST /api/auth/apple/` - Apple Sign-In authentication
- `POST /api/auth/token/` - Get JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Tenant Management
- `GET /api/tenants/` - Get current tenant details
- `GET /api/tenants/policies/` - Get tenant policies
- `PUT /api/tenants/policies/<key>/` - Update tenant policy (Admin)

### Profile Management
- `GET /api/profiles/` - List profiles in current tenant
- `POST /api/profiles/` - Create new profile (Admin)
- `GET /api/profiles/<id>/` - Get profile details
- `PUT /api/profiles/<id>/` - Update profile (Admin)
- `DELETE /api/profiles/<id>/` - Delete profile (Admin)
- `POST /api/profiles/<id>/assign/` - Assign users to profile (Admin)

### Admin
- `GET /api/admin/stats/` - Get platform statistics
- `GET /api/admin/users/` - List users (Admin)
- `PUT /api/admin/users/<id>/` - Update user (Admin)
- `GET /api/admin/audit-logs/` - Get audit logs (Admin)

## Webhooks
- `/webhooks/profile-change/` - Notifies when profile permissions change
- `/webhooks/tenant-policy-update/` - Notifies when tenant policies are updated