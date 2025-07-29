# Audio Streaming Tests

This directory contains comprehensive unit and integration tests for the audio streaming module.

## Test Files

### Unit Tests

1. **test_tts.py** - Tests for Text-to-Speech functionality
   - Tests gTTS integration
   - Error handling (empty text, broken pipe, gTTS errors)
   - Different languages support
   - Edge cases (whitespace-only text, long text)

2. **test_hls.py** - Tests for HLS (HTTP Live Streaming) writer
   - StreamingHLSWriter initialization and directory creation
   - FFmpeg process management
   - Audio chunk processing
   - Playlist finalization
   - Error handling and process restart logic

3. **test_pipeline.py** - Tests for audio generation pipeline
   - Basic audio session flow
   - Text chunk logging functionality
   - Multiple chunk processing
   - FFmpeg process monitoring and restart
   - LLM integration and error handling
   - First chunk optimization

4. **test_views.py** - Tests for API endpoints
   - `/audiostream/start/` endpoint (start_audio_session)
   - `/audiostream/task-status/<task_id>/` endpoint (task_status)
   - Async vs sync execution modes
   - Redis availability handling
   - Error responses
   - Integration between endpoints

5. **test_tasks.py** - Tests for Celery tasks
   - generate_audio_stream task execution
   - Progress callback functionality
   - Timeout handling
   - Thread management
   - Error handling in background tasks
   - Custom parameters support

### Integration Tests

6. **test_integration.py** - End-to-end integration tests
   - Complete audio generation flow
   - Task status progression
   - Error handling throughout pipeline
   - Concurrent sessions
   - Text logging integration
   - Invalid request handling
   - Sync fallback scenarios
   - Real-world user workflows
   - Multilingual support

## Running the Tests

### Run all tests:
```bash
make test
```

### Run specific test file:
```bash
python -m pytest talemo/audiostream/tests/test_tts.py -v
```

### Run specific test class:
```bash
python -m pytest talemo/audiostream/tests/test_views.py::TestStartAudioSessionView -v
```

### Run specific test method:
```bash
python -m pytest talemo/audiostream/tests/test_tts.py::TestTTSFunctions::test_speak_chunk_to_ffmpeg_success -v
```

### Run with coverage:
```bash
make coverage
```

## Test Coverage

The test suite covers:
- Success paths for all major functions
- Error handling and edge cases
- Mocking of external dependencies (Redis, Celery, FFmpeg, gTTS, LLM)
- Integration scenarios
- Concurrent request handling
- File I/O operations
- Task state management
- API request/response validation

## Mocking Strategy

The tests use extensive mocking to:
- Avoid dependencies on external services
- Ensure fast test execution
- Test error conditions that would be hard to reproduce
- Isolate components for true unit testing

Key mocked components:
- Redis connections
- Celery task execution
- FFmpeg subprocess
- gTTS service
- LLM token generation
- File system operations (where appropriate)
- Django ORM operations

## Test Data

Tests use minimal, focused test data:
- Simple prompts for audio generation
- Mock session IDs
- Simulated task states
- Example playlist URLs
- Test audio data (mocked as bytes)