from unittest import mock
import asyncio
import os
import pytest

# Mock the OpenAI client before importing any modules that use it
mock_openai = mock.patch('openai.AsyncOpenAI').start()

# Create a simple test that doesn't rely on mocking the StreamingHLSWriter
def test_pipeline_simple():
    """Test that the pipeline module can be imported and the run_audio_session function exists."""
    from talemo.audiostream.pipeline import run_audio_session
    assert callable(run_audio_session)

    # Test that the function has the expected signature
    import inspect
    sig = inspect.signature(run_audio_session)
    assert 'prompt' in sig.parameters
    assert 'playlist_path' in sig.parameters
    assert 'lang' in sig.parameters
    assert 'chunk_words' in sig.parameters
    assert 'progress_cb' in sig.parameters
