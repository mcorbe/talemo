# Talemo - Technical Implementation Document

## 1. Document Control

| Item          | Value                                           |
| ------------- | ----------------------------------------------- |
| **Product**   | Talemo - Family Audio-Stories Platform          |
| **Version**   | 2.0                                             |
| **Author**    | Engineering Team                                |
| **Date**      | Based on PRD v3 (2025)                          |
| **Reviewers** | CTO, Product Team, DevOps, Security             |

---

## 2. System Architecture Overview

### 2.1 High-Level Architecture

Talemo follows a modern, scalable architecture with these key components:

``` 
┌─────────────────┐     ┌─────────────────────────────┐     ┌────────────────────────────┐
│  Client Layer   │     │      Service Layer          │     │      Data Layer            │
├─────────────────┤     ├─────────────────────────────┤     ├────────────────────────────┤
│ - PWA           │     │ - Django MVT                │     │ - PostgreSQL (RLS)         │
│ - Capacitor App │     │ - Django REST               │     │ - pgvector Extension       │
│ - HTMX + BS5    │◄───►│ - Multi-Tenant Middleware   │◄───►│ - MinIO/S3 (tenant-prefix) │
│                 │     │ - Profile-Based Permissions │     │ - Redis                    │
│                 │     │ - Celery                    │     │ - WORM Audit Storage       │
│                 │     │ - CrewAI Agents             │     │                            │
│                 │     │ - RAG Pipeline              │     │                            │
└─────────────────┘     └─────────────────────────────┘     └────────────────────────────┘
```

### 2.2 Component Details

1. **Frontend**:
   - Progressive Web App (PWA) with offline capabilities
   - HTMX for dynamic interactions without full page reloads
   - Bootstrap 5 for responsive, mobile-first design
   - CapacitorJS for native app wrappers (iOS/Android)
   - Tenant-aware UI with profile-based feature visibility
   - Dark-screen mode ("Mode Conte") for screen-free listening

2. **Backend**:
   - Django (MVT) for server-side rendering and admin interface
   - Django REST Framework for API endpoints
   - Multi-tenant middleware for tenant context management
   - Profile-based permission system
   - Celery for asynchronous task processing
   - CrewAI for agent-based content generation and workflows
   - RAG Pipeline for semantic search and duplication detection
   - Vector embeddings for story content and search queries

3. **Data Storage**:
   - PostgreSQL with Row-Level Security (RLS) for tenant isolation
   - pgvector extension for vector embeddings storage and similarity search
   - Tenant-prefixed MinIO/S3 paths for media asset isolation
   - WORM (Write Once Read Many) storage for immutable audit logs
   - Redis for caching and Celery message broker
   - 100% data hosted in France with SecNumCloud certification

4. **Authentication & Identity**:
   - Django-allauth for SSO integration (Google & Apple)
   - UserIdentity model for IDP linking with tenant binding
   - JWT for API authentication with tenant context
   - Profile-based permission system (replacing RBAC)
   - Tenant invitation flow with secure token generation

5. **Governance & Compliance**:
   - TenantPolicy key-value store for tenant-wide settings
   - Profile catalogue for permission templates
   - Audit logging for all governance actions
   - SECNUMCLOUD (ANSSI) compliance controls
   - CNIL-compliant consent management for children under 15

6. **Deployment**:
   - Docker containers for all components
   - Kubernetes-ready for cloud deployment
   - French cloud hosting for data sovereignty
   - Tenant-aware scaling and resource allocation

---

## 3. Database Schema

### 3.1 Core Entities

#### Tenant
```
Tenant
├── id: UUID (PK)
├── name: CharField
├── type: CharField [family, institution]
├── created_at: DateTimeField
└── updated_at: DateTimeField
```

#### Profile
```
Profile
├── id: UUID (PK)
├── tenant_id: ForeignKey(Tenant)
├── name: CharField (unique within tenant)
├── permissions: JSONField
├── created_at: DateTimeField
└── updated_at: DateTimeField
```

#### User
```
User
├── id: UUID (PK)
├── tenant_id: ForeignKey(Tenant)
├── profile_id: ForeignKey(Profile)
├── email: EmailField
├── name: CharField
├── is_active: BooleanField
├── created_at: DateTimeField
└── last_login: DateTimeField
```

#### UserIdentity
```
UserIdentity
├── id: UUID (PK)
├── user_id: ForeignKey(User)
├── idp_issuer: CharField
├── idp_subject: CharField
├── created_at: DateTimeField
└── metadata: JSONField
```

#### TenantPolicy
```
TenantPolicy
├── id: UUID (PK)
├── tenant_id: ForeignKey(Tenant)
├── key: CharField (unique within tenant)
├── value: JSONField
├── created_at: DateTimeField
└── updated_at: DateTimeField
```

#### Story
```
Story
├── id: UUID (PK)
├── tenant_id: ForeignKey(Tenant)
├── title: CharField
├── description: TextField
├── content: TextField (story text)
├── image: ForeignKey(Asset)
├── audio: ForeignKey(Asset)
├── user_audio: ForeignKey(Asset, null=True) # For record-your-own narration
├── language: CharField
├── age_range: CharField [0-3, 4-6, 7-9, 10-12, 13+]
├── duration: IntegerField (seconds)
├── tags: ManyToManyField(Tag)
├── created_by: ForeignKey(User)
├── visibility: CharField [public, tenant_only, private]
├── is_published: BooleanField
├── is_ai_generated: BooleanField # For AI Act compliance
├── created_at: DateTimeField
└── updated_at: DateTimeField
```

#### Asset
```
Asset
├── id: UUID (PK)
├── tenant_id: ForeignKey(Tenant)
├── type: CharField [image, audio, user_audio]
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
├── tenant_id: ForeignKey(Tenant)
├── agent_type: CharField [ModerationAgent, TTSAgent, IllustratorAgent, QuotaAgent, EmbeddingAgent, StoryCompanion]
├── status: CharField [pending, processing, completed, failed]
├── input: JSONField
├── output: JSONField
├── error: TextField (null=True)
├── created_at: DateTimeField
├── started_at: DateTimeField (null=True)
├── completed_at: DateTimeField (null=True)
├── token_usage: JSONField # For cost tracking
└── model_used: CharField # For fallback tracking
```

#### Subscription
```
Subscription
├── id: UUID (PK)
├── tenant_id: ForeignKey(Tenant)
├── user: ForeignKey(User)
├── plan: CharField [free, creator_premium]
├── status: CharField [active, canceled, expired]
├── start_date: DateTimeField
├── end_date: DateTimeField (null=True)
└── payment_provider: CharField
```

#### ParentalConsent
```
ParentalConsent
├── id: UUID (PK)
├── tenant_id: ForeignKey(Tenant)
├── user_id: ForeignKey(User) # Child user
├── consenting_user_id: ForeignKey(User) # Parent user
├── consent_type: CharField [app_usage, data_processing, recording]
├── status: CharField [granted, revoked]
├── created_at: DateTimeField
└── updated_at: DateTimeField
```

### 3.2 Relationships

- Tenant 1:N Profile (one tenant can have many profiles)
- Tenant 1:N User (one tenant can have many users)
- Tenant 1:N Story (one tenant can have many stories)
- Tenant 1:N Asset (one tenant can have many assets)
- Tenant 1:N TenantPolicy (one tenant can have many policies)
- Profile N:M User (users can be assigned to profiles)
- User 1:N UserIdentity (one user can have multiple identity providers)
- User 1:N Story (one user can create many stories)
- Story N:1 Image Asset (one story has one main image)
- Story N:1 Audio Asset (one story has one audio file)
- Story N:1 User Audio Asset (one story can have one user-recorded audio)
- Story N:M Tag (stories can have multiple tags)
- AgentTask 1:N Asset (one agent task can generate multiple assets)
- User 1:N ParentalConsent (one parent can consent for multiple children)

All tenant-bound tables share the same Row-Level Security (RLS) predicate: `USING (tenant_id = current_setting('app.tenant')::uuid)`

---

## 4. API Design

### 4.1 REST API Endpoints

#### Authentication
- `POST /api/auth/google/` - Google SSO authentication
- `POST /api/auth/apple/` - Apple Sign-In authentication
- `POST /api/auth/token/` - Get JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token

#### Stories
- `GET /api/stories/` - List stories (with filtering by tags, age_range, language, visibility)
- `GET /api/stories/<id>/` - Get story details
- `POST /api/stories/` - Create story (requires appropriate profile permissions)
- `PUT /api/stories/<id>/` - Update story (creator or admin)
- `PATCH /api/stories/<id>/visibility/` - Update story visibility [public, tenant_only, private]
- `DELETE /api/stories/<id>/` - Delete story (admin)
- `GET /api/stories/search/` - Search stories

#### Assets
- `GET /api/assets/<id>/` - Get asset details (tenant-scoped)
- `GET /api/assets/<id>/download/` - Get signed URL for asset download (tenant-scoped)
- `POST /api/assets/` - Upload asset (requires appropriate profile permissions)
- `POST /api/assets/record-audio/` - Upload user-recorded audio for a story
- `DELETE /api/assets/<id>/` - Delete asset (admin)
- `GET /api/assets/tenant-usage/` - Get storage usage statistics for current tenant

#### Agent Tasks
- `POST /api/agents/trigger/` - Trigger agent task (tenant-scoped, requires appropriate profile permissions)
- `GET /api/agents/tasks/<id>/` - Get task status (tenant-scoped)
- `GET /api/agents/tasks/` - List tasks for current tenant (admin)
- `GET /api/agents/quota/` - Get agent usage quota information for current tenant
- `POST /api/agents/story-companion/` - Interact with StoryCompanion agent

#### Tenant Management
- `GET /api/tenants/` - Get current tenant details
- `GET /api/tenants/policies/` - Get tenant policies
- `PUT /api/tenants/policies/<key>/` - Update tenant policy (Admin)

#### Profile Management
- `GET /api/profiles/` - List profiles in current tenant
- `POST /api/profiles/` - Create new profile (Admin)
- `GET /api/profiles/<id>/` - Get profile details
- `PUT /api/profiles/<id>/` - Update profile (Admin)
- `DELETE /api/profiles/<id>/` - Delete profile (Admin)
- `POST /api/profiles/<id>/assign/` - Assign users to profile (Admin)

#### Parental Controls
- `GET /api/parental-controls/` - Get parental control settings
- `PUT /api/parental-controls/` - Update parental control settings
- `POST /api/parental-controls/consent/` - Provide parental consent
- `GET /api/parental-controls/activity/` - Get child activity report

#### Subscription Management
- `GET /api/subscriptions/` - Get current subscription details
- `POST /api/subscriptions/` - Create new subscription
- `PUT /api/subscriptions/<id>/` - Update subscription
- `DELETE /api/subscriptions/<id>/` - Cancel subscription

#### Admin
- `GET /api/admin/stats/` - Get platform statistics
- `GET /api/admin/users/` - List users (Admin)
- `PUT /api/admin/users/<id>/` - Update user (Admin)
- `GET /api/admin/audit-logs/` - Get audit logs (Admin)

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
- `/webhooks/audit-event/` - Streams governance and security audit events
- `/webhooks/profile-change/` - Notifies when profile permissions change
- `/webhooks/tenant-policy-update/` - Notifies when tenant policies are updated

---

## 5. Authentication & Authorization

### 5.1 Authentication Flow

1. **SSO Implementation**:
   - Implement Google and Apple Sign-In using django-allauth
   - Configure OAuth2 client IDs and secrets
   - Set up callback URLs and handle token exchange
   - Store identity provider information in UserIdentity model

2. **JWT for API Access**:
   - Issue JWT tokens upon successful authentication
   - Include tenant_id and profile permissions in token payload
   - Implement token refresh mechanism
   - Enforce tenant context in all API requests

3. **Mobile Authentication**:
   - Web: Standard OAuth2 flow
   - Native apps: Use Capacitor plugins for native auth dialogs
   - Maintain consistent identity across platforms

4. **Identity Uniqueness**:
   - Enforce global uniqueness of (idp_issuer, idp_subject) pairs
   - Allow multiple IDPs per user if they map to the same tenant
   - Prevent cross-tenant identity conflicts

### 5.2 Profile-Based Access Control

The system uses a profile-based permission system instead of per-user role assignments:

1. **Profile Management**:
   - Tenant admins create and manage permission profiles (e.g., "Kids Listen-Only", "Parent Creator")
   - Profiles contain a JSON structure of permissions and quotas
   - Users are assigned to profiles, not individual permissions

2. **Permission Enforcement**:
   - Permissions are loaded from Profile.permissions JSON once per request
   - All access checks reference the profile permissions
   - No per-user permission tweaking allowed

3. **Tenant Policies**:
   - Global tenant settings stored in TenantPolicy KV store
   - Examples: story_quota, max_users, feature_flags
   - Applied uniformly to all users within a tenant

### 5.3 Multi-Tenant Implementation

1. **Row-Level Security**:
   - PostgreSQL RLS policies on all tenant-bound tables
   - Predicate: `USING (tenant_id = current_setting('app.tenant')::uuid)`
   - Set tenant context at the beginning of each request

2. **Tenant Isolation**:
   - Middleware sets app.tenant based on authenticated user
   - Database queries automatically filtered by tenant_id
   - Storage paths prefixed with tenant_id

3. **Audit Trail**:
   - All profile/policy changes logged to immutable storage
   - Audit records include tenant_id, user_id, action, timestamp
   - Retention period of at least 1 year for compliance

### 5.4 Parental Consent Management

1. **CNIL-Compliant Consent**:
   - Explicit parental consent required for users under 15
   - Granular consent options for different data processing activities
   - Consent records stored in ParentalConsent table
   - Audit trail of all consent changes

2. **Consent Verification**:
   - Email verification for parental consent
   - Periodic re-confirmation of consent
   - Option to revoke consent at any time

---

## 6. Agent Architecture Implementation

### 6.1 CrewAI Integration

The agent architecture will be implemented using CrewAI, with Django as the orchestration layer:

```
┌─────────────────────────────────────────────────────────┐
│                      Django Application                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │  API Layer  │───►│Celery Tasks │───►│ Agent Bridge│  │
│  └─────────────┘    └─────────────┘    └──────┬──────┘  │
│                                               │         │
└───────────────────────────────────────────────┼─────────┘
                                                ▼
┌─────────────────────────────────────────────────────────┐
│                     CrewAI Framework                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │StoryCompanion│──►│  TTS Agent  │───►│ Image Agent │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                         │
│                     ┌─────────────┐                     │
│                     │Moderation   │                     │
│                     │Agent        │                     │
│                     └─────────────┘                     │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Agent Implementation

#### ModerationAgent
- **Purpose**: Ensures content safety and appropriateness
- **Input**: Story draft, tenant context
- **Process**: Runs GPT-4 based moderation & keyword heuristics
- **Output**: Approval status or flagged content
- **Event Flow**: Consumes `story.draft` → Produces `story.approved` or `story.flagged`

#### TTSAgent
- **Purpose**: Converts text to speech
- **Input**: Approved story text, voice parameters
- **Process**: Synthesizes speech via tenant-selected French voice pack
- **Output**: Audio file in MP3 format stored in MinIO
- **Event Flow**: Consumes `story.approved` → Produces `asset.audio.ready`

#### IllustratorAgent
- **Purpose**: Generates illustrations for stories
- **Input**: Approved story text, style parameters
- **Process**: Generates cover art using Stable Diffusion XL
- **Output**: Image file in PNG format stored under tenant prefix
- **Event Flow**: Consumes `story.approved` → Produces `asset.image.ready`

#### QuotaAgent
- **Purpose**: Enforces tenant quotas
- **Input**: Story creation request, tenant context
- **Process**: Checks TenantPolicy.story_quota
- **Output**: Approval or rejection based on quota
- **Event Flow**: Consumes `story.request`

#### EmbeddingAgent
- **Purpose**: Generates vector embeddings for semantic search and duplication detection
- **Input**: Story draft
- **Process**: Creates vector embeddings using LlamaIndex and stores them in pgvector
- **Output**: Vector embeddings stored in database
- **Event Flow**: Consumes `story.draft` → Produces `story.embedded` or `story.duplicate`

### 6.3 User-Facing Agents

#### StoryCompanion
- **Purpose**: Co-creation chat assistant for families
- **Implementation**: Chat interface with CrewAI backend
- **Features**: Suggests themes, characters, helps develop story
- **Workflow**: Chat → Fill Details → Generate → Preview → Save to Library
- **Event Flow**: Consumes user input → Produces structured story form

### 6.4 Agent Communication

- REST API between Django and CrewAI
- Message passing via Redis for agent-to-agent communication
- State management in PostgreSQL (AgentTask table)

### 6.5 Cost Control Implementation

1. **Model & Voice Caching**:
   - Aggressive caching of TTS outputs for common phrases
   - Library of pre-generated voice clips for story templates
   - Voice fingerprinting to avoid regenerating similar audio

2. **Local Inference**:
   - Client-side TTS for select devices with sufficient capabilities
   - Hybrid approach with on-device generation for common content

3. **Model Optimization**:
   - Fine-tuned smaller LLMs for children's story generation
   - Prompt optimization techniques to reduce token usage
   - Story templates that require minimal LLM customization

4. **Token Usage Tracking**:
   - Per-request token counting
   - Cost calculation based on current model pricing
   - Budget alerts and quota enforcement

### 6.6 Semantic Story Search Implementation with LlamaIndex

1. **LlamaIndex RAG Pipeline**:
   - Implement LlamaIndex as the core RAG (Retrieval Augmented Generation) framework
   - Use LlamaIndex's document processing pipeline for story content ingestion
   - Leverage LlamaIndex's query engine for semantic search capabilities
   - Implement LlamaIndex's vector store integration with pgvector

2. **Vector Database Integration**:
   - Implement pgvector extension for PostgreSQL
   - Store story embeddings as vector data generated by LlamaIndex
   - Configure vector similarity search (cosine similarity)
   - Use LlamaIndex's PGVectorStore for seamless integration

3. **Search Algorithm**:
   - Convert search queries to vector embeddings using LlamaIndex's embedding models
   - Rank results by cosine similarity through LlamaIndex's retriever components
   - Implement full-text fallback for edge cases
   - Combine semantic and keyword matching for optimal results
   - Use LlamaIndex's hybrid search capabilities for both semantic and keyword matching

4. **Performance Optimization**:
   - Implement vector indexing for fast similarity search
   - Cache common search queries
   - Batch process embeddings generation with LlamaIndex's batch processing capabilities
   - Monitor and tune `shared_buffers` for optimal performance
   - Leverage LlamaIndex's metadata filtering for efficient query narrowing

5. **User Experience**:
   - Natural language search interface powered by LlamaIndex
   - Contextual search suggestions
   - Search filters (age range, duration, themes) implemented as metadata filters
   - Search history for quick access to previous queries

### 6.7 Duplication Guard Implementation with LlamaIndex

1. **Similarity Detection with LlamaIndex**:
   - Compare new story embeddings against existing library using LlamaIndex's similarity search
   - Leverage LlamaIndex's vector store query capabilities for efficient similarity comparison
   - Set configurable similarity threshold (initially 0.85)
   - Flag potential duplicates for review
   - Use LlamaIndex's embedding models for consistent vector representation

2. **Workflow Integration**:
   - Check for duplicates during story creation process using LlamaIndex's retrieval pipeline
   - Provide feedback to users when duplicates are detected
   - Allow parental override for false positives
   - Log override decisions to tune threshold
   - Integrate with EmbeddingAgent's LlamaIndex pipeline

3. **Optimization Strategy**:
   - Implement batch processing for large libraries using LlamaIndex's batch inference
   - Use LlamaIndex's approximate nearest neighbor search capabilities for efficiency
   - Tune similarity threshold based on user feedback
   - Auto-whitelist after parental override
   - Leverage LlamaIndex's metadata filtering to narrow search scope

4. **Monitoring & Tuning**:
   - Track false positive and false negative rates
   - Weekly adjustment of similarity threshold
   - Monitor performance impact on database
   - Implement batch processing for cold-start scenarios
   - Use LlamaIndex's evaluation metrics to assess duplication detection quality

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

### 7.3 « Mode Conte » Implementation

1. **Dark-Screen Mode**:
   - One-tap activation to blank the display
   - Keep audio controls accessible
   - Lock screen integration for playback control
   - Battery optimization during audio-only playback

2. **Technical Implementation**:
   - CSS transitions for screen dimming
   - Media Session API for lock screen controls
   - Background audio playback service
   - Wake lock prevention

3. **User Experience**:
   - Simple toggle between visual and audio-only modes
   - Gesture controls for basic playback functions
   - Voice feedback for navigation in audio-only mode

### 7.4 Record-Your-Own Implementation

1. **Audio Recording Interface**:
   - Simple, child-friendly recording controls
   - Visual cues for recording progress
   - Playback and re-recording options
   - Text highlighting for reading guidance

2. **Technical Implementation**:
   - Web Audio API for browser recording
   - Native audio recording via Capacitor plugins
   - Waveform visualization for recording feedback
   - Client-side audio processing for quality improvement

3. **Storage and Playback**:
   - User recordings stored as alternate audio tracks
   - Option to switch between AI and user narration
   - Offline availability of user recordings
   - Secure storage with tenant isolation

### 7.5 Offline Capabilities

1. **Story Caching**:
   - Downloadable story packs for offline use
   - Automatic caching of recently played stories
   - Background downloading of selected content

2. **Sync Management**:
   - Queue changes made offline for sync when online
   - Conflict resolution for concurrent edits
   - Progress tracking across devices

---

## 8. Development Roadmap

### 8.1 4-Month MVP Timeline

#### Weeks 1-4: Core Infrastructure
- Set up multi-tenant architecture with RLS
- Implement basic authentication and profile system
- Create initial story playback functionality
- Configure French data hosting with SecNumCloud compliance

#### Weeks 5-8: Story Creation
- Implement AI story generation workflow
- Integrate French voice packs
- Develop basic moderation system
- Submit CNIL DPIA (Data Protection Impact Assessment)

#### Weeks 9-12: Key Features
- Implement record-your-own functionality
- Develop « Mode Conte » (dark-screen mode)
- Create offline capabilities
- Implement parental consent management

#### Weeks 13-16: QA & Launch Prep
- Perform performance optimization
- Conduct final UI/UX refinement
- Complete security audit
- Prepare app store submission
- Launch beta with 100 French families

### 8.2 Post-MVP Priorities

1. Enhanced analytics for retention optimization
2. Advanced parental controls and family management features
3. Additional cost optimization implementations
4. Family sharing and collaboration features
5. Premium voice packs with French celebrity narrators

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
- CNIL compliance testing

---

## 10. Deployment Strategy

### 10.1 Infrastructure Requirements

- Kubernetes cluster in French data centers
- PostgreSQL database with SecNumCloud certification
- Object storage (S3/MinIO) in France
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

### 10.4 AI Observability Implementation

#### 10.4.1 OpenTelemetry Integration

- Implement CrewAI's built-in OpenTelemetry instrumentation
- Configure OTel collectors for span collection and export
- Define custom attributes for tenant context and agent metadata
- Implement trace context propagation across agent workflows

#### 10.4.2 Token Usage & Cost Tracking

- Instrument all LLM calls to track token usage
- Implement per-model, per-tenant, and per-request token counting
- Set up cost calculation based on current model pricing
- Create tenant-specific usage dashboards and reports
- Implement budget alerts and quota enforcement

#### 10.4.3 Observability Platform Integration

1. **Development Environment**:
   - Integrate Arize Phoenix for local development and testing
   - Implement one-line instrumentation: `CrewAIInstrumentor().instrument()`
   - Set up local UI at http://localhost:6006 for trace visualization

2. **Production Environment**:
   - Implement Langfuse integration for production telemetry
   - Configure OpenLIT integration with `openlit.init(tracer=langfuse._otel_tracer)`
   - Set up cost tracking and latency monitoring
   - Implement prompt versioning and evaluation

3. **Agent Performance Analysis**:
   - Integrate AgentOps for session replays and run comparisons
   - Implement side-by-side diffing for agent iteration analysis
   - Set up performance benchmarking for agent workflows

4. **Fallback Monitoring**:
   - Track primary and fallback service usage
   - Monitor success rates and latency differences
   - Implement automatic alerting for fallback activations

#### 10.4.4 Privacy & Compliance

- Implement PII redaction in all telemetry data
- Ensure GDPR and COPPA compliance in observability data
- Configure immutable WORM storage for AI operation logs
- Implement retention policies aligned with compliance requirements

---

## 11. Security Considerations

### 11.1 Data Protection

- Encryption at rest for all data
- TLS for all communications
- Secure asset storage with signed URLs and tenant prefixes
- GDPR and CNIL compliance measures for children under 15
- SECNUMCLOUD (ANSSI) compliance controls
- 100% data hosted in France

### 11.2 Multi-Tenant Security

- Row-level security (RLS) for all tenant-bound tables
- Tenant context set at the beginning of each request
- Tenant isolation enforced at database level
- Storage isolation with tenant-specific prefixes
- Immutable audit logs for tenant operations

### 11.3 Identity Management

- Global uniqueness of (idp_issuer, idp_subject) pairs
- Tenant-bound identity linking
- Composite DB constraint to prevent cross-tenant identity conflicts
- Secure invitation flow with tenant_id embedding

### 11.4 Authentication Security

- OAuth2 best practices
- JWT token security (short expiry, refresh tokens)
- Tenant context included in token payload
- Rate limiting for authentication endpoints
- Account lockout after failed attempts

### 11.5 Application Security

- Input validation and sanitization
- CSRF protection
- XSS prevention
- SQL injection protection
- Regular security audits
- WORM (Write Once Read Many) storage for audit trails

### 11.6 Parental Controls & Child Safety

- Age-appropriate content filtering
- Parental approval workflow for story creation
- Activity monitoring and reporting for parents
- Granular consent management
- Content moderation for user-generated recordings

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

### 13.2 Payment Processors

- Stripe for subscription management
- Apple In-App Purchases (for iOS app)
- Google Play Billing (for Android app)

### 13.3 AI Services

- LlamaIndex for RAG (Retrieval Augmented Generation) pipeline and semantic search
- Text-to-Speech providers with French voice packs
- Image generation services
- Content moderation APIs
- Fallback services for each AI component

### 13.4 Hardware Partnerships

- SDK integration for Lunii devices
- API for Yoto integration
- Content export for Tonies

---

## 14. Business Model Implementation

### 14.1 Creator Premium Subscription

- €3.99/month subscription implementation
- Unlimited story creation for subscribers
- Ad-free experience
- Premium voice packs and illustration styles
- Offline story packs

### 14.2 Free Tier Limitations

- 5 rotating AI-generated stories per week
- 2 story creations per week
- Basic voice and illustration options
- Limited offline capabilities

### 14.3 Quota Management

- Story creation quota tracking
- Voice generation limits
- Image generation limits
- Storage quotas

### 14.4 Conversion Optimization

- Strategic conversion prompts at engagement points
- Free trial implementation
- Family sharing incentives
- Subscription management interface

### 14.5 Analytics & Metrics Tracking

1. **Key Performance Indicators**:
   - Implement tracking for all success metrics defined in PRD
   - Set up dashboards for real-time monitoring
   - Configure alerts for metrics falling below targets

2. **Search Performance Metrics**:
   - Track Search-to-Play conversion rate (target ≥ 55%)
   - Measure query relevance and result quality
   - Monitor search latency and optimization opportunities
   - Analyze search patterns to improve content recommendations

3. **Content Quality Metrics**:
   - Track Duplicate stories generated per 1,000 prompts (target ≤ 1.0)
   - Monitor false positive and false negative rates for duplication detection
   - Implement feedback loop for improving similarity threshold
   - Log parental overrides to tune the system

4. **Cost Efficiency Metrics**:
   - Track Average TTS cost per story (target ≤ €0.062)
   - Monitor token usage across different models
   - Measure cache hit rates for voice and model outputs
   - Analyze cost reduction from optimization strategies

5. **Implementation Details**:
   - Event-based tracking system for user interactions
   - Aggregation pipeline for metrics calculation
   - Tenant-specific analytics with appropriate isolation
   - GDPR-compliant data collection and retention

---

## 15. Conclusion & Next Steps

This technical implementation document provides a comprehensive roadmap for building the Talemo platform based on the PRD v3 requirements. The architecture is designed to be scalable, secure, and maintainable, with a focus on:

1. French-first, mobile-first user experience
2. AI-powered content generation with cost optimization
3. Multi-tenant governance and strict data sovereignty
4. Creator-led subscription model
5. CNIL compliance and child safety

### Key Architectural Decisions:

1. **Multi-Tenant Architecture**: Strict tenant isolation using PostgreSQL Row-Level Security and tenant-prefixed storage paths
2. **Profile-Based Permissions**: Replacing traditional RBAC with a more flexible and manageable profile-based system
3. **Identity Management**: Global uniqueness of identity provider credentials with tenant binding
4. **Agent-Based Workflows**: Stateless, tenant-scoped agents for content generation, moderation, and personalization
5. **LlamaIndex RAG Pipeline**: Semantic search and duplication detection using LlamaIndex with pgvector integration
6. **Compliance-Ready Design**: Architecture mapped to SECNUMCLOUD controls with audit trails and immutable logs
7. **French Data Residency**: 100% data hosted in France with SecNumCloud certification

### Immediate Next Steps:

1. **Technical Validation**: Proof-of-concept for CrewAI + Celery integration with tenant context
2. **LlamaIndex RAG POC**: Validate LlamaIndex integration with pgvector for semantic search
3. **Multi-Tenant POC**: Validate Profile & RLS scaffold with sample load test
4. **Development Environment**: Set up initial project structure and Docker environment
5. **Team Onboarding**: Brief development team on architecture and roadmap
6. **Sprint Planning**: Break down Phase 1 tasks into sprint-sized work items
7. **CNIL Compliance**: Prepare DPIA submission and SecNumCloud certification process

The implementation will follow an agile approach, with regular reviews and adjustments to the plan as development progresses. The 4-month MVP timeline is aggressive but achievable with the focused scope outlined in the PRD v3.
