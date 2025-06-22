# Talemo Application Package

This directory contains the main application package for the Talemo platform. It follows a domain-driven design approach, with separate modules for different functional areas of the application.

## Overview

The Talemo application is organized into domain-specific modules, each responsible for a specific aspect of the platform's functionality. This modular approach promotes separation of concerns, maintainability, and testability.

## Module Structure

Each module follows a similar internal structure:

- `models/`: Data models and database schema
- `views/`: Django views for rendering templates
- `api/`: REST API endpoints
- `services/`: Business logic and services
- `tasks/`: Celery tasks for asynchronous processing
- `templates/`: Module-specific templates (if not in the central templates directory)

## Modules

### core

The `core` module provides fundamental functionality used throughout the application:

- Multi-tenant infrastructure
- User authentication and profiles
- Permissions and access control
- Common utilities and middleware

### stories

The `stories` module manages the creation, storage, and playback of audio stories:

- Story data models
- Story creation workflows
- Story browsing and discovery
- Story playback functionality

### agents

The `agents` module implements the AI agent framework using CrewAI:

- Agent definitions and configurations
- Agent tasks and workflows
- CrewAI integration
- Agent playground functionality

### assets

The `assets` module handles media asset management:

- Audio file storage and processing
- Image storage and processing
- MinIO/S3 integration
- Asset metadata management

### governance

The `governance` module provides compliance and governance features:

- Audit logging
- Content moderation
- Policy enforcement
- Reporting and analytics

### subscriptions

The `subscriptions` module manages user subscriptions and billing:

- Subscription plans and pricing
- Billing integration
- Usage tracking
- Payment processing

## Inter-Module Communication

Modules communicate with each other through well-defined interfaces:

- Direct imports for tightly coupled functionality
- Signals for event-based communication
- Celery tasks for asynchronous processing
- REST API for loosely coupled integration

## Development Guidelines

When working with the application package:

1. Maintain separation of concerns between modules
2. Use explicit imports (avoid wildcard imports)
3. Keep circular dependencies to a minimum
4. Document public APIs and interfaces
5. Write tests for all new functionality
6. Follow the established code style and patterns

## Related Documentation

For more detailed information about specific modules, refer to their individual documentation:

- [Core Module Documentation](core/README.md)
- [Stories Module Documentation](stories/README.md)
- [Agents Module Documentation](agents/README.md)
- [Assets Module Documentation](assets/README.md)
- [Governance Module Documentation](governance/README.md)
- [Subscriptions Module Documentation](subscriptions/README.md)