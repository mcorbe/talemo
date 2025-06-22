# Talemo - Technical Implementation Document

## 1. Document Control

| Item          | Value                                           |
| ------------- | ----------------------------------------------- |
| **Product**   | Talemo - Family Audio-Stories Platform          |
| **Version**   | 1.0                                             |
| **Author**    | Engineering Team                                |
| **Date**      | Based on PRD v0.3 (22 Jun 2025)                 |
| **Reviewers** | CTO, Product Team, DevOps, Security             |

---

## 2. System Architecture Overview

### 2.1 High-Level Architecture

Talemo follows a modern, scalable architecture with these key components:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Client Layer   │     │  Service Layer  │     │   Data Layer    │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ - PWA           │     │ - Django MVT    │     │ - PostgreSQL    │
│ - Capacitor App │     │ - Django REST   │     │ - MinIO/S3      │
│ - HTMX + BS5    │◄───►│ - Celery        │◄───►│ - Redis         │
│                 │     │ - CrewAI        │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 2.2 Component Details

1. **Frontend**:
   - Progressive Web App (PWA) with offline capabilities
   - HTMX for dynamic interactions without full page reloads
   - Bootstrap 5 for responsive, mobile-first design
   - CapacitorJS for native app wrappers (iOS/Android)

2. **Backend**:
   - Django (MVT) for server-side rendering and admin interface
   - Django REST Framework for API endpoints
   - Celery for asynchronous task processing
   - CrewAI for agent-based content generation and workflows

3. **Data Storage**:
   - PostgreSQL for relational data
   - MinIO for local development/on-prem storage of media assets
   - Redis for caching and Celery message broker

4. **Authentication**:
   - Django-allauth for SSO integration (Google & Apple)
   - JWT for API authentication
   - Role-based access control (RBAC)

5. **Deployment**:
   - Docker containers for all components
   - Kubernetes-ready for cloud deployment
   - Cloud-agnostic design (AWS/GCP/Azure compatible)

---

## 3. Database Schema

### 3.1 Core Entities

#### User
```
User
├── id: UUID (PK)
├── email: EmailField (unique)
├── name: CharField
├── role: CharField [Guest, Registered, Creator, Admin]
├── auth_provider: CharField [Google, Apple, Email]
├── is_active: BooleanField
├── created_at: DateTimeField
└── last_login: DateTimeField
```

#### Story
```
Story
├── id: UUID (PK)
├── title: CharField
├── description: TextField
├── content: TextField (story text)
├── image: ForeignKey(Asset)
├── audio: ForeignKey(Asset)
├── language: CharField
├── age_range: CharField [0-3, 4-6, 7-9, 10-12, 13+]
├── duration: IntegerField (seconds)
├── tags: ManyToManyField(Tag)
├── created_by: ForeignKey(User)
├── is_published: BooleanField
├── created_at: DateTimeField
└── updated_at: DateTimeField
```

#### Asset
```
Asset
├── id: UUID (PK)
├── type: CharField [image, audio]
├── file_path: CharField
├── file_size: IntegerField
├── mime_type: CharField
├── source_task: ForeignKey(AgentTask, null=True)
├── created_at: DateTimeField
└── metadata: JSONField
```

#### Tag
```
Tag
├── id: UUID (PK)
├── name: CharField
├── slug: SlugField
└── category: CharField [theme, character, mood, etc.]
```

#### AgentTask
```
AgentTask
├── id: UUID (PK)
├── agent_type: CharField [StoryBuilder, TTS, ImageGen, Metadata, Moderation]
├── status: CharField [pending, processing, completed, failed]
├── input: JSONField
├── output: JSONField
├── error: TextField (null=True)
├── created_at: DateTimeField
├── started_at: DateTimeField (null=True)
└── completed_at: DateTimeField (null=True)
```

#### Subscription
```
Subscription
├── id: UUID (PK)
├── user: ForeignKey(User)
├── plan: CharField [free, premium, institution]
├── status: CharField [active, canceled, expired]
├── start_date: DateTimeField
├── end_date: DateTimeField (null=True)
└── payment_provider: CharField
```

### 3.2 Relationships

- User 1:N Story (one user can create many stories)
- Story N:1 Image Asset (one story has one main image)
- Story N:1 Audio Asset (one story has one audio file)
- Story N:M Tag (stories can have multiple tags)
- AgentTask 1:N Asset (one agent task can generate multiple assets)

---

## 4. API Design

### 4.1 REST API Endpoints

#### Authentication
- `POST /api/auth/google/` - Google SSO authentication
- `POST /api/auth/apple/` - Apple Sign-In authentication
- `POST /api/auth/token/` - Get JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token

#### Stories
- `GET /api/stories/` - List stories (with filtering)
- `GET /api/stories/<id>/` - Get story details
- `POST /api/stories/` - Create story (Creator/Admin)
- `PUT /api/stories/<id>/` - Update story (Creator/Admin)
- `DELETE /api/stories/<id>/` - Delete story (Admin)
- `GET /api/stories/search/` - Search stories

#### Assets
- `GET /api/assets/<id>/` - Get asset details
- `GET /api/assets/<id>/download/` - Get signed URL for asset download
- `POST /api/assets/` - Upload asset (Creator/Admin)
- `DELETE /api/assets/<id>/` - Delete asset (Admin)

#### Agent Tasks
- `POST /api/agents/trigger/` - Trigger agent task
- `GET /api/agents/tasks/<id>/` - Get task status
- `GET /api/agents/tasks/` - List tasks (Admin)

#### Admin
- `GET /api/admin/stats/` - Get platform statistics
- `GET /api/admin/users/` - List users (Admin)
- `PUT /api/admin/users/<id>/` - Update user (Admin)

### 4.2 API Response Format

Standard JSON response format:

```json
{
  "status": "success|error",
  "data": { ... },
  "message": "Optional message",
  "errors": { ... }
}
```

### 4.3 Webhooks

- `/webhooks/agent-task-complete/` - Notifies when an agent task completes
- `/webhooks/subscription-status/` - Subscription status changes

---

## 5. Authentication & Authorization

### 5.1 Authentication Flow

1. **SSO Implementation**:
   - Implement Google and Apple Sign-In using django-allauth
   - Configure OAuth2 client IDs and secrets
   - Set up callback URLs and handle token exchange

2. **JWT for API Access**:
   - Issue JWT tokens upon successful authentication
   - Include user role and permissions in token payload
   - Implement token refresh mechanism

3. **Mobile Authentication**:
   - Web: Standard OAuth2 flow
   - Native apps: Use Capacitor plugins for native auth dialogs

### 5.2 Role-Based Access Control (RBAC)

| Role        | Permissions                                                   |
|-------------|---------------------------------------------------------------|
| Guest       | Browse public stories, play limited number of stories         |
| Registered  | Access all stories based on subscription, save favorites      |
| Creator     | Create and edit own stories, trigger agent workflows          |
| Admin       | Full CRUD access to all resources, user management            |

### 5.3 Implementation Details

- Use Django's permission system extended with custom permissions
- Implement middleware for role-based access checks
- Create decorators for view-level permission checks
- Set up row-level permissions for story ownership

---

## 6. Agent Architecture Implementation

### 6.1 CrewAI Integration

The agent architecture will be implemented using CrewAI, with Django as the orchestration layer:

```
┌─────────────────────────────────────────────────────────┐
│                      Django Application                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │  API Layer  │───►│Celery Tasks │───►│ Agent Bridge│  │
│  └─────────────┘    └─────────────┘    └──────┬──────┘  │
│                                               │         │
└───────────────────────────────────────────────┼─────────┘
                                                ▼
┌─────────────────────────────────────────────────────────┐
│                     CrewAI Framework                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │Story Builder│───►│  TTS Agent  │───►│ Image Agent │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐                     │
│  │Metadata Agent◄───┤Moderation   │                     │
│  └─────────────┘    │Agent        │                     │
│                     └─────────────┘                     │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Agent Implementation

#### StoryBuilderAgent
- **Purpose**: Orchestrates the story creation workflow
- **Input**: Story text, target age range, theme
- **Process**: Coordinates other agents, manages workflow
- **Output**: Complete story package (text, audio, image, metadata)

#### TTSAgent
- **Purpose**: Converts text to speech
- **Input**: Story text, voice parameters
- **Process**: Uses TTS service (local or third-party)
- **Output**: Audio file in MP3 format

#### ImageGenAgent
- **Purpose**: Generates illustrations for stories
- **Input**: Story text, scene description
- **Process**: Uses image generation model
- **Output**: Illustration image in appropriate format

#### MetadataAgent
- **Purpose**: Auto-tags and categorizes stories
- **Input**: Story text, audio duration
- **Process**: Analyzes content for themes, characters, mood
- **Output**: Tags, age recommendations, categories

#### ModerationAgent
- **Purpose**: Ensures content safety
- **Input**: Story text, generated images
- **Process**: Checks for inappropriate content
- **Output**: Safety score, flags for manual review if needed

### 6.3 User-Facing Agents

#### StoryCompanion
- **Purpose**: Interactive story co-creation
- **Implementation**: Chat interface with CrewAI backend
- **Features**: Suggests plot elements, characters, helps develop story

#### SearchAssistant
- **Purpose**: Conversational search for stories
- **Implementation**: Natural language query processing
- **Features**: Understands intent, suggests relevant stories

### 6.4 Agent Communication

- REST API between Django and CrewAI
- Message passing via Redis for agent-to-agent communication
- State management in PostgreSQL (AgentTask table)

---

## 7. Mobile App Strategy

### 7.1 PWA Implementation

1. **Core Technologies**:
   - Django templates for server-side rendering
   - HTMX for dynamic content without full page reloads
   - Bootstrap 5 for responsive design
   - Service Worker for offline capabilities

2. **PWA Features**:
   - App manifest for home screen installation
   - Offline story playback
   - Push notifications (where supported)
   - Responsive design for all screen sizes

3. **Performance Optimizations**:
   - Image optimization and lazy loading
   - Audio streaming with adaptive bitrate
   - Critical CSS inlining
   - Asset caching strategies

### 7.2 Native App Wrappers (CapacitorJS)

1. **Implementation Approach**:
   - Use CapacitorJS to wrap the PWA
   - Add native plugins for enhanced functionality
   - Configure for App Store and Play Store distribution

2. **Native Features**:
   - Native audio playback controls
   - Background audio
   - Native push notifications
   - Native share dialogs
   - Deep linking

3. **Platform-Specific Considerations**:
   - iOS: Meet App Store guidelines
   - Android: Optimize for diverse devices
   - Both: Implement native SSO flows

### 7.3 Shared Codebase Strategy

- Single source of truth in Django templates
- Responsive design system with mobile-first approach
- Feature detection for progressive enhancement
- Unified asset pipeline for web and mobile

---

## 8. Development Roadmap

### 8.1 Phase 1: Foundation (Weeks 1-4)

1. **Setup Development Environment**:
   - Configure Django project structure
   - Set up Docker development environment
   - Configure CI/CD pipeline

2. **Core Data Model Implementation**:
   - Implement database schema
   - Create Django models
   - Set up migrations

3. **Authentication System**:
   - Implement SSO with Google and Apple
   - Set up RBAC system
   - Create JWT authentication for API

4. **Basic Frontend**:
   - Implement responsive templates
   - Set up HTMX integration
   - Create basic UI components

### 8.2 Phase 2: Core Functionality (Weeks 5-8)

1. **Story Management**:
   - Implement story CRUD operations
   - Create story listing and detail views
   - Implement search and filtering

2. **Asset Management**:
   - Set up MinIO integration
   - Implement asset upload/download
   - Create signed URL generation

3. **Agent Framework Integration**:
   - Set up CrewAI integration
   - Implement basic agent tasks
   - Create agent task monitoring

4. **Admin Interface**:
   - Customize Django admin
   - Create admin dashboard
   - Implement user management

### 8.3 Phase 3: Advanced Features (Weeks 9-12)

1. **Story Generation Workflow**:
   - Implement full agent pipeline
   - Create story creation interface
   - Set up asynchronous processing

2. **PWA Implementation**:
   - Add service worker
   - Implement offline capabilities
   - Create app manifest

3. **User-Facing Agents**:
   - Implement StoryCompanion
   - Create SearchAssistant
   - Set up conversational interfaces

4. **Subscription System**:
   - Implement subscription plans
   - Create payment integration
   - Set up access control based on subscription

### 8.4 Phase 4: Mobile & Polish (Weeks 13-16)

1. **CapacitorJS Integration**:
   - Set up Capacitor project
   - Integrate native plugins
   - Configure for app stores

2. **Performance Optimization**:
   - Optimize asset loading
   - Implement caching strategies
   - Tune database queries

3. **Testing & QA**:
   - Comprehensive testing
   - User acceptance testing
   - Performance benchmarking

4. **Documentation & Deployment**:
   - Create deployment documentation
   - Prepare for production
   - Final security audit

---

## 9. Testing Strategy

### 9.1 Testing Levels

1. **Unit Testing**:
   - Django model tests
   - API endpoint tests
   - Agent function tests
   - Use pytest for test framework

2. **Integration Testing**:
   - API integration tests
   - Agent workflow tests
   - Authentication flow tests

3. **End-to-End Testing**:
   - User journey tests
   - Mobile app tests
   - Cypress for web E2E testing

4. **Performance Testing**:
   - Load testing with Locust
   - Mobile performance testing
   - Database query optimization

### 9.2 Test Automation

- CI/CD pipeline integration
- Automated test runs on pull requests
- Test coverage reporting
- Performance regression testing

### 9.3 Quality Assurance

- Manual testing checklist
- Accessibility testing (WCAG 2.1)
- Cross-browser and cross-device testing
- Security testing (OWASP Top 10)

---

## 10. Deployment Strategy

### 10.1 Infrastructure Requirements

- Kubernetes cluster (or equivalent)
- PostgreSQL database
- Object storage (S3/GCS/Azure Blob/MinIO)
- Redis instance
- Load balancer with SSL termination

### 10.2 Deployment Pipeline

1. **Build Stage**:
   - Build Docker images
   - Run tests
   - Static analysis

2. **Staging Deployment**:
   - Deploy to staging environment
   - Run integration tests
   - Performance testing

3. **Production Deployment**:
   - Blue/green deployment
   - Database migrations
   - Cache warming

4. **Post-Deployment**:
   - Smoke tests
   - Monitoring check
   - Rollback plan if needed

### 10.3 Monitoring & Operations

- Application monitoring (Prometheus + Grafana)
- Error tracking (Sentry)
- Log aggregation (ELK stack)
- Alerting system
- Backup and disaster recovery plan

---

## 11. Security Considerations

### 11.1 Data Protection

- Encryption at rest for all data
- TLS for all communications
- Secure asset storage with signed URLs
- GDPR and COPPA compliance measures

### 11.2 Authentication Security

- OAuth2 best practices
- JWT token security (short expiry, refresh tokens)
- Rate limiting for authentication endpoints
- Account lockout after failed attempts

### 11.3 Application Security

- Input validation and sanitization
- CSRF protection
- XSS prevention
- SQL injection protection
- Regular security audits

---

## 12. Scalability Considerations

### 12.1 Database Scalability

- Connection pooling
- Read replicas for heavy read operations
- Partitioning strategy for large tables
- Query optimization

### 12.2 Application Scalability

- Stateless application design
- Horizontal scaling of web servers
- Celery worker scaling based on queue size
- Caching strategy (Redis)

### 12.3 Storage Scalability

- CDN integration for assets
- Object storage tiering
- Lifecycle policies for old assets
- Compression for audio/image assets

---

## 13. Third-Party Integrations

### 13.1 Authentication Providers

- Google OAuth2
- Apple Sign-In
- (Future) SAML/OIDC providers

### 13.2 Payment Processors

- Stripe for subscription management
- PayPal as alternative payment method
- Apple In-App Purchases (for iOS app)
- Google Play Billing (for Android app)

### 13.3 AI Services

- Text-to-Speech providers
- Image generation services
- Content moderation APIs
- Fallback services for each AI component

---

## 14. Conclusion & Next Steps

This technical implementation document provides a comprehensive roadmap for building the Talemo platform. The architecture is designed to be scalable, secure, and maintainable, with a focus on mobile-first user experience and AI-powered content generation.

### Immediate Next Steps:

1. **Technical Validation**: Proof-of-concept for CrewAI + Celery integration
2. **Development Environment**: Set up initial project structure and Docker environment
3. **Team Onboarding**: Brief development team on architecture and roadmap
4. **Sprint Planning**: Break down Phase 1 tasks into sprint-sized work items

The implementation will follow an agile approach, with regular reviews and adjustments to the plan as development progresses.