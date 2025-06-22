# Assets Module

This module handles media asset management, including audio file storage and processing, image storage and processing, MinIO/S3 integration, and asset metadata management.

## Models

- **Asset**
  - `id`: UUID (PK)
  - `tenant_id`: ForeignKey(Tenant)
  - `type`: CharField [image, audio, user_audio]
  - `file_path`: CharField
  - `file_size`: IntegerField
  - `mime_type`: CharField
  - `source_task`: ForeignKey(AgentTask, null=True)
  - `created_at`: DateTimeField
  - `metadata`: JSONField

## URLs

- `/api/assets/<id>/` - Get asset details
- `/api/assets/<id>/download/` - Get signed URL for asset download
- `/api/assets/` - Upload asset
- `/api/assets/record-audio/` - Upload user-recorded audio for a story
- `/api/assets/<id>/` - Delete asset
- `/api/assets/tenant-usage/` - Get storage usage statistics

## Views

- Asset detail view
- Asset upload view
- User audio recording view
- Asset download view
- Tenant storage usage view

## API Endpoints

### Assets
- `GET /api/assets/<id>/` - Get asset details (tenant-scoped)
- `GET /api/assets/<id>/download/` - Get signed URL for asset download (tenant-scoped)
- `POST /api/assets/` - Upload asset (requires appropriate profile permissions)
- `POST /api/assets/record-audio/` - Upload user-recorded audio for a story
- `DELETE /api/assets/<id>/` - Delete asset (admin)
- `GET /api/assets/tenant-usage/` - Get storage usage statistics for current tenant

## Storage Implementation

- Tenant-prefixed MinIO/S3 paths for media asset isolation
- Secure asset storage with signed URLs
- Tenant-specific storage quotas
- Audio file optimization and compression
- Image optimization for different device sizes

## Record-Your-Own Implementation

- Simple, child-friendly recording interface
- Web Audio API for browser recording
- Native audio recording via Capacitor plugins
- Waveform visualization for recording feedback
- Client-side audio processing for quality improvement
- User recordings stored as alternate audio tracks
- Option to switch between AI and user narration
- Offline availability of user recordings
- Secure storage with tenant isolation