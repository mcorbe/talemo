# Agents Module

This module implements the AI agent framework using CrewAI, including agent definitions and configurations, agent tasks and workflows, CrewAI integration, and agent playground functionality.

## Models

- **AgentTask**
  - `id`: UUID (PK)
  - `tenant_id`: ForeignKey(Tenant)
  - `agent_type`: CharField [ModerationAgent, TTSAgent, IllustratorAgent, QuotaAgent, EmbeddingAgent, StoryCompanion]
  - `status`: CharField [pending, processing, completed, failed]
  - `input`: JSONField
  - `output`: JSONField
  - `error`: TextField (null=True)
  - `created_at`: DateTimeField
  - `started_at`: DateTimeField (null=True)
  - `completed_at`: DateTimeField (null=True)
  - `token_usage`: JSONField # For cost tracking
  - `model_used`: CharField # For fallback tracking

## URLs

- `/api/agents/trigger/` - Trigger agent task
- `/api/agents/tasks/<id>/` - Get task status
- `/api/agents/tasks/` - List tasks
- `/api/agents/quota/` - Get agent usage quota
- `/api/agents/story-companion/` - Interact with StoryCompanion agent

## Views

- Agent playground view
- Agent task status view
- Agent quota view
- StoryCompanion interaction view

## API Endpoints

### Agent Tasks
- `POST /api/agents/trigger/` - Trigger agent task (tenant-scoped, requires appropriate profile permissions)
- `GET /api/agents/tasks/<id>/` - Get task status (tenant-scoped)
- `GET /api/agents/tasks/` - List tasks for current tenant (admin)
- `GET /api/agents/quota/` - Get agent usage quota information for current tenant
- `POST /api/agents/story-companion/` - Interact with StoryCompanion agent

## Agent Types

### ModerationAgent
- **Purpose**: Ensures content safety and appropriateness
- **Input**: Story draft, tenant context
- **Process**: Runs GPT-4 based moderation & keyword heuristics
- **Output**: Approval status or flagged content
- **Event Flow**: Consumes `story.draft` → Produces `story.approved` or `story.flagged`

### TTSAgent
- **Purpose**: Converts text to speech
- **Input**: Approved story text, voice parameters
- **Process**: Synthesizes speech via tenant-selected French voice pack
- **Output**: Audio file in MP3 format stored in MinIO
- **Event Flow**: Consumes `story.approved` → Produces `asset.audio.ready`

### IllustratorAgent
- **Purpose**: Generates illustrations for stories
- **Input**: Approved story text, style parameters
- **Process**: Generates cover art using Stable Diffusion XL
- **Output**: Image file in PNG format stored under tenant prefix
- **Event Flow**: Consumes `story.approved` → Produces `asset.image.ready`

### QuotaAgent
- **Purpose**: Enforces tenant quotas
- **Input**: Story creation request, tenant context
- **Process**: Checks TenantPolicy.story_quota
- **Output**: Approval or rejection based on quota
- **Event Flow**: Consumes `story.request`

### EmbeddingAgent
- **Purpose**: Generates vector embeddings for semantic search and duplication detection
- **Input**: Story draft
- **Process**: Creates vector embeddings using LlamaIndex and stores them in pgvector
- **Output**: Vector embeddings stored in database
- **Event Flow**: Consumes `story.draft` → Produces `story.embedded` or `story.duplicate`

### StoryCompanion
- **Purpose**: Co-creation chat assistant for families
- **Implementation**: Chat interface with CrewAI backend
- **Features**: Suggests themes, characters, helps develop story
- **Workflow**: Chat → Fill Details → Generate → Preview → Save to Library
- **Event Flow**: Consumes user input → Produces structured story form

## CrewAI Integration

The agent architecture is implemented using CrewAI, with Django as the orchestration layer:

- API Layer in Django communicates with Celery Tasks
- Celery Tasks communicate with Agent Bridge
- Agent Bridge interfaces with CrewAI Framework
- CrewAI Framework manages various agents (StoryCompanion, TTS Agent, Image Agent, Moderation Agent)

## Cost Control Implementation

- Model & Voice Caching for common phrases
- Local Inference for select devices
- Model Optimization with fine-tuned smaller LLMs
- Token Usage Tracking for budget management

## Webhooks

- `/webhooks/agent-task-complete/` - Notifies when an agent task completes