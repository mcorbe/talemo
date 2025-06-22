# Governance Module

This module provides compliance and governance features, including audit logging, content moderation, policy enforcement, and reporting and analytics.

## Models

- **ParentalConsent**
  - `id`: UUID (PK)
  - `tenant_id`: ForeignKey(Tenant)
  - `user_id`: ForeignKey(User) # Child user
  - `consenting_user_id`: ForeignKey(User) # Parent user
  - `consent_type`: CharField [app_usage, data_processing, recording]
  - `status`: CharField [granted, revoked]
  - `created_at`: DateTimeField
  - `updated_at`: DateTimeField

## URLs

- `/api/parental-controls/` - Get/update parental control settings
- `/api/parental-controls/consent/` - Provide parental consent
- `/api/parental-controls/activity/` - Get child activity report
- `/api/admin/audit-logs/` - Get audit logs

## Views

- Parental controls view
- Consent management view
- Activity reporting view
- Audit log view

## API Endpoints

### Parental Controls
- `GET /api/parental-controls/` - Get parental control settings
- `PUT /api/parental-controls/` - Update parental control settings
- `POST /api/parental-controls/consent/` - Provide parental consent
- `GET /api/parental-controls/activity/` - Get child activity report

### Admin
- `GET /api/admin/audit-logs/` - Get audit logs (Admin)

## Parental Consent Management

- CNIL-Compliant Consent for users under 15
- Granular consent options for different data processing activities
- Consent records stored in ParentalConsent table
- Audit trail of all consent changes
- Email verification for parental consent
- Periodic re-confirmation of consent
- Option to revoke consent at any time

## Audit Logging

- All profile/policy changes logged to immutable storage
- Audit records include tenant_id, user_id, action, timestamp
- Retention period of at least 1 year for compliance
- WORM (Write Once Read Many) storage for immutable audit logs

## Content Moderation

- Age-appropriate content filtering
- Parental approval workflow for story creation
- Activity monitoring and reporting for parents
- Content moderation for user-generated recordings

## Webhooks

- `/webhooks/audit-event/` - Streams governance and security audit events