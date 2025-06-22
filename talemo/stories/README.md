# Stories Module

This module manages the creation, storage, and playback of audio stories, including story data models, story creation workflows, story browsing and discovery, and story playback functionality.

## Models

- **Story**
  - `id`: UUID (PK)
  - `tenant_id`: ForeignKey(Tenant)
  - `title`: CharField
  - `description`: TextField
  - `content`: TextField (story text)
  - `image`: ForeignKey(Asset)
  - `audio`: ForeignKey(Asset)
  - `user_audio`: ForeignKey(Asset, null=True) # For record-your-own narration
  - `language`: CharField
  - `age_range`: CharField [0-3, 4-6, 7-9, 10-12, 13+]
  - `duration`: IntegerField (seconds)
  - `tags`: ManyToManyField(Tag)
  - `created_by`: ForeignKey(User)
  - `visibility`: CharField [public, tenant_only, private]
  - `is_published`: BooleanField
  - `is_ai_generated`: BooleanField # For AI Act compliance
  - `created_at`: DateTimeField
  - `updated_at`: DateTimeField

- **Tag**
  - `id`: UUID (PK)
  - `name`: CharField
  - `slug`: SlugField
  - `category`: CharField [theme, character, mood, etc.]

## URLs

- `/api/stories/` - List stories
- `/api/stories/<id>/` - Get story details
- `/api/stories/` - Create story
- `/api/stories/<id>/` - Update story
- `/api/stories/<id>/visibility/` - Update story visibility
- `/api/stories/<id>/` - Delete story
- `/api/stories/search/` - Search stories

## Views

- Story list view
- Story detail view
- Story creation view
- Story edit view
- Story search view
- Story playback view
- Story library view

## API Endpoints

### Stories
- `GET /api/stories/` - List stories (with filtering by tags, age_range, language, visibility)
- `GET /api/stories/<id>/` - Get story details
- `POST /api/stories/` - Create story (requires appropriate profile permissions)
- `PUT /api/stories/<id>/` - Update story (creator or admin)
- `PATCH /api/stories/<id>/visibility/` - Update story visibility [public, tenant_only, private]
- `DELETE /api/stories/<id>/` - Delete story (admin)
- `GET /api/stories/search/` - Search stories

## Search Implementation

The stories module implements a semantic search capability using LlamaIndex:

- LlamaIndex RAG Pipeline for story content ingestion
- Vector embeddings stored in pgvector extension
- Semantic search using vector similarity
- Hybrid search combining semantic and keyword matching
- Search filters for age range, duration, themes, etc.
- Natural language search interface

## Duplication Guard

The stories module includes a duplication detection system:

- Similarity detection using LlamaIndex and vector embeddings
- Configurable similarity threshold (initially 0.85)
- Workflow integration during story creation
- Parental override for false positives
- Monitoring and tuning of similarity thresholds