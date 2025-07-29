# Demo Audio Page - Backend Integration Documentation

## Overview

The `demo_audio.html` page is a demonstration interface for the Talemo audio streaming system. It showcases how to integrate with the backend's real-time audio generation and HLS streaming capabilities.

## Architecture Flow

```
[Frontend]          [Django Backend]         [Celery Worker]        [Storage]
    |                     |                        |                    |
    |--POST /start/------>|                        |                    |
    |                     |--queue task----------->|                    |
    |<--{task_id}---------|                        |                    |
    |                     |                        |--generate audio--->|
    |--GET /task-status-->|                        |                    |
    |<--{state,progress}--|                        |--write segments--->|
    |                     |                        |                    |
    |--GET .m3u8 playlist-|----------------------->|                    |
    |--GET .m4s segments--|----------------------->|                    |
```

## Backend Endpoints Used

### 1. Start Audio Session: `POST /audiostream/start/`

**Purpose**: Initiates an audio generation session from a text prompt.

**Request**:
```json
{
  "prompt": "Hello!",
  "lang": "en"  // optional, defaults to "en"
}
```

**Response**:
```json
{
  "session_id": "abc123...",
  "playlist": "/media/hls/abc123.../audio.m3u8",
  "task_id": "abc123..."
}
```

**Backend Processing**:
1. Receives the prompt and language
2. Generates a unique session ID
3. Checks if Celery/Redis is available for async processing
4. If async is available:
   - Queues a `generate_audio_stream` Celery task
   - Returns immediately with task ID and predicted playlist URL
5. If async is not available:
   - Runs the task synchronously (fallback mode)
   - Returns the result directly

### 2. Check Task Status: `GET /audiostream/task-status/<task_id>/`

**Purpose**: Monitors the progress of the audio generation task.

**Response States**:

- **PENDING**: Task is queued but not started
  ```json
  {
    "state": "PENDING",
    "status": "Task is pending"
  }
  ```

- **PROGRESS**: Task is actively processing
  ```json
  {
    "state": "PROGRESS",
    "status": "Task is in progress",
    "event": "chunk",
    "chunk_count": 5
  }
  ```

- **SUCCESS**: Task completed successfully
  ```json
  {
    "state": "SUCCESS",
    "status": "Task completed successfully",
    "result": {
      "playlist": "/media/hls/abc123.../audio.m3u8"
    },
    "playlist": "/media/hls/abc123.../audio.m3u8"
  }
  ```

- **FAILURE**: Task failed
  ```json
  {
    "state": "FAILURE",
    "status": "Task failed",
    "error": "Error message here"
  }
  ```

## Frontend Implementation Details

### 1. Audio Generation Flow

1. **User Action**: User enters text in textarea and clicks "Start" button
2. **Request Submission**: Frontend sends POST request to `/audiostream/start/`
3. **Initial Response**: Backend returns task ID and playlist URL
4. **Progress Monitoring**: Frontend polls `/audiostream/task-status/<task_id>/` every second
5. **Player Initialization**: Once playlist URL is available, HLS.js player is initialized

### 2. HLS Player Configuration

The demo uses **HLS.js** library with low-latency optimizations:

```javascript
const hls = new Hls({
  lowLatencyMode: true,              // Enable low latency mode
  liveSyncDurationCount: 3,          // Segments to keep in sync
  maxBufferLength: 10,               // Reduced buffer for lower latency
  startFragPrefetch: true,           // Prefetch fragments
  manifestLoadingMaxRetry: 8,        // Retry attempts for streaming
});
```

### 3. Error Handling & Retry Logic

The frontend implements robust retry mechanisms:

- **Empty Playlist Retries**: Up to 15 attempts with exponential backoff
- **Manifest Load Retries**: Up to 15 attempts for network errors
- **Native HLS Fallback**: For Safari/iOS devices without HLS.js support

### 4. Progress Visualization

The demo includes:
- Status messages with color-coded states (loading, playing, error)
- Progress bar showing percentage completion
- Real-time chunk processing updates

## Backend Processing Pipeline

### 1. Celery Task: `generate_audio_stream`

Located in `talemo/audiostream/tasks.py`:

1. **Session Creation**: Creates unique session ID and storage path
2. **Database Update**: Creates/updates AudioSession record
3. **HLS Writer Setup**: Initializes StreamingHLSWriter for segment creation
4. **Background Processing**: Runs audio generation in separate thread
5. **Progress Updates**: Reports progress via Celery's update_state

### 2. Audio Processing Pipeline

The pipeline (`run_audio_session` in `pipeline.py`):

1. **Text Processing**: 
   - If prompt, processes through LLM for expansion
   - Chunks text into smaller segments

2. **Audio Generation**:
   - Each chunk converted to speech using gTTS
   - Audio encoded to AAC format

3. **HLS Streaming**:
   - Audio segments written as .m4s files
   - Playlist (.m3u8) updated incrementally
   - Segments immediately available for streaming

### 3. Storage Management

- **Local Storage**: Files stored in `media/hls/<session_id>/`
- **MinIO Support**: Can be configured for S3-compatible storage
- **Segment Files**: audio_000.m4s, audio_001.m4s, etc.
- **Playlist File**: audio.m3u8 (master playlist)

## Key Features Demonstrated

1. **Real-time Streaming**: Audio segments are available as soon as they're generated
2. **Progressive Loading**: Users can start listening before generation completes
3. **Error Recovery**: Automatic retries for network and processing failures
4. **Cross-browser Support**: Works with both HLS.js and native HLS implementations
5. **Status Tracking**: Real-time progress updates during generation

## Configuration Requirements

### Django Settings
```python
# HLS URL prefix for serving media files
HLS_URL = "/media/hls/"

# Celery configuration for async processing
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
```

### Required Services
- **Redis**: For Celery task queue and result backend
- **Celery Worker**: For async audio generation
- **Media Server**: To serve HLS files (Django's development server or nginx)

## Security Considerations

1. **CSRF Protection**: Frontend includes CSRF token in POST requests
2. **Permissions**: Currently uses `AllowAny` for demo purposes
3. **Session Management**: Each audio generation gets unique session ID
4. **Resource Limits**: Consider implementing rate limiting for production

## Usage Example

```javascript
// Start audio generation
const response = await fetch('/audiostream/start/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCsrfToken()
  },
  body: JSON.stringify({
    prompt: 'Tell me a short story about a brave knight',
    lang: 'en'
  })
});

const { task_id, playlist } = await response.json();

// Monitor progress
const checkStatus = async () => {
  const status = await fetch(`/audiostream/task-status/${task_id}/`);
  const data = await status.json();
  
  if (data.state === 'SUCCESS') {
    // Initialize HLS player with playlist URL
    initializePlayer(data.playlist);
  } else if (data.state === 'PROGRESS') {
    // Show progress to user
    updateProgress(data.chunk_count);
    // Continue polling
    setTimeout(checkStatus, 1000);
  }
};

checkStatus();
```

## Performance Characteristics

- **Initial Response Time**: < 500ms (task queuing)
- **First Audio Segment**: 2-5 seconds (depends on text length)
- **Segment Duration**: 2 seconds per segment (configurable)
- **Concurrent Sessions**: Limited by Celery worker count
- **Memory Usage**: ~50MB per active session

## Troubleshooting Common Issues

1. **"No playlist URL in response"**: Check if Celery/Redis is running
2. **"Playlist remains empty"**: Verify FFmpeg is installed and accessible
3. **"Task status PENDING forever"**: Ensure Celery workers are running
4. **"Playback stalled"**: Check if segments are being generated (view logs)
5. **"CORS errors"**: Configure CORS headers for cross-origin requests