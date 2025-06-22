# Subscriptions Module

This module manages user subscriptions and billing, including subscription plans and pricing, billing integration, usage tracking, and payment processing.

## Models

- **Subscription**
  - `id`: UUID (PK)
  - `tenant_id`: ForeignKey(Tenant)
  - `user`: ForeignKey(User)
  - `plan`: CharField [free, creator_premium]
  - `status`: CharField [active, canceled, expired]
  - `start_date`: DateTimeField
  - `end_date`: DateTimeField (null=True)
  - `payment_provider`: CharField

## URLs

- `/api/subscriptions/` - Get current subscription details
- `/api/subscriptions/` - Create new subscription
- `/api/subscriptions/<id>/` - Update subscription
- `/api/subscriptions/<id>/` - Cancel subscription

## Views

- Subscription management view
- Subscription details view
- Payment processing view
- Subscription upgrade/downgrade view

## API Endpoints

### Subscription Management
- `GET /api/subscriptions/` - Get current subscription details
- `POST /api/subscriptions/` - Create new subscription
- `PUT /api/subscriptions/<id>/` - Update subscription
- `DELETE /api/subscriptions/<id>/` - Cancel subscription

## Business Model Implementation

### Creator Premium Subscription
- €3.99/month subscription implementation
- Unlimited story creation for subscribers
- Ad-free experience
- Premium voice packs and illustration styles
- Offline story packs

### Free Tier Limitations
- 5 rotating AI-generated stories per week
- 2 story creations per week
- Basic voice and illustration options
- Limited offline capabilities

### Quota Management
- Story creation quota tracking
- Voice generation limits
- Image generation limits
- Storage quotas

### Conversion Optimization
- Strategic conversion prompts at engagement points
- Free trial implementation
- Family sharing incentives
- Subscription management interface

## Payment Integrations

- Stripe for subscription management
- Apple In-App Purchases (for iOS app)
- Google Play Billing (for Android app)

## Webhooks

- `/webhooks/subscription-status/` - Subscription status changes