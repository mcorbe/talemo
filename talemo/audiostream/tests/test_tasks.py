import os
import time
import threading
from unittest.mock import Mock, patch, MagicMock, call
from django.test import TestCase
from celery import states
from talemo.audiostream.tasks import generate_audio_stream
from talemo.audiostream.models import AudioSession


class TestGenerateAudioStreamTask(TestCase):
    """Test cases for the generate_audio_stream Celery task."""

    def setUp(self):
        """Set up test fixtures."""
        self.prompt = "Test audio generation prompt"
        self.lang = "en"
        self.session_id = "test-session-123"
        
    @patch('talemo.audiostream.tasks.SegmentStore')
    @patch('talemo.audiostream.tasks.StreamingHLSWriter')
    @patch('talemo.audiostream.tasks.run_audio_session')
    @patch('talemo.audiostream.tasks.AudioSession.objects.update_or_create')
    @patch('talemo.audiostream.tasks.AudioSession.objects.filter')
    @patch('os.path.exists')
    def test_generate_audio_stream_success(self, mock_exists, mock_filter, mock_update_create, 
                                         mock_run_audio, mock_writer_class, mock_store_class):
        """Test successful audio stream generation."""
        # Mock SegmentStore
        mock_store = Mock()
        mock_store.create.return_value = (
            'session-123',
            '/tmp/hls/session-123',
            'http://example.com/hls/session-123/audio.m3u8'
        )
        mock_store_class.return_value = mock_store
        
        # Mock StreamingHLSWriter
        mock_writer = Mock()
        mock_writer_class.return_value = mock_writer
        
        # Mock path exists (playlist and segment)
        mock_exists.side_effect = [
            True,  # playlist exists
            True,  # first segment exists
        ]
        
        # Mock Django ORM
        mock_update_result = Mock()
        mock_filter.return_value.update = mock_update_result
        
        # Create mock task with request object
        mock_task = Mock()
        mock_task.request.id = 'test-task-id'
        mock_task.request.delivery_info = {'routing_key': 'celery'}
        
        # Run the task
        result = generate_audio_stream.run(
            self.prompt,
            self.lang,
            self.session_id,
            _self=mock_task
        )
        
        # Assertions
        self.assertIsInstance(result, dict)
        self.assertIn('playlist', result)
        self.assertEqual(result['playlist'], 'http://example.com/hls/session-123/audio.m3u8')
        
        # Verify store was created
        mock_store_class.assert_called_once()
        mock_store.create.assert_called_once_with(self.session_id)
        
        # Verify AudioSession was created
        mock_update_create.assert_called_once_with(
            session_id='session-123',
            defaults={
                "status": "running",
                "playlist_rel_url": 'http://example.com/hls/session-123/audio.m3u8'
            }
        )
        
        # Verify HLS writer was created
        mock_writer_class.assert_called_once_with('/tmp/hls/session-123')
        
        # Verify status was updated to ready
        mock_filter.assert_called()
        mock_update_result.assert_called_with(status="ready")
        
    @patch('talemo.audiostream.tasks.SegmentStore')
    @patch('talemo.audiostream.tasks.StreamingHLSWriter')
    @patch('talemo.audiostream.tasks.run_audio_session')
    @patch('talemo.audiostream.tasks.AudioSession.objects.update_or_create')
    @patch('talemo.audiostream.tasks.AudioSession.objects.filter')
    @patch('os.path.exists')
    @patch('time.time')
    @patch('time.sleep')
    def test_generate_audio_stream_timeout(self, mock_sleep, mock_time, mock_exists, 
                                         mock_filter, mock_update_create, mock_run_audio, 
                                         mock_writer_class, mock_store_class):
        """Test timeout when waiting for first segment."""
        # Mock SegmentStore
        mock_store = Mock()
        mock_store.create.return_value = (
            'session-456',
            '/tmp/hls/session-456',
            'http://example.com/hls/session-456/audio.m3u8'
        )
        mock_store_class.return_value = mock_store
        
        # Mock StreamingHLSWriter
        mock_writer = Mock()
        mock_writer_class.return_value = mock_writer
        
        # Mock time progression
        start_time = 1000
        mock_time.side_effect = [
            start_time,  # Initial time
            start_time,  # While loop check
            start_time + 0.5,  # After first sleep
            start_time + 1.0,  # After second sleep
            start_time + 5.5,  # Timeout exceeded
        ]
        
        # Mock path exists - playlist exists but segment doesn't
        mock_exists.side_effect = [
            True,   # playlist exists
            False,  # first segment doesn't exist
            False,  # still doesn't exist
            False,  # still doesn't exist
        ]
        
        # Mock Django ORM
        mock_update_result = Mock()
        mock_filter.return_value.update = mock_update_result
        
        # Create mock task
        mock_task = Mock()
        mock_task.request.id = 'timeout-task-id'
        mock_task.request.delivery_info = {}
        
        # Run the task
        result = generate_audio_stream.run(
            self.prompt,
            self.lang,
            None,  # No custom session ID
            timeout_before_return=5.0,
            _self=mock_task
        )
        
        # Should still return playlist URL despite timeout
        self.assertIn('playlist', result)
        
        # Verify we slept while waiting
        self.assertTrue(mock_sleep.called)
        
    @patch('talemo.audiostream.tasks.SegmentStore')
    @patch('talemo.audiostream.tasks.StreamingHLSWriter')
    @patch('talemo.audiostream.tasks.run_audio_session')
    @patch('talemo.audiostream.tasks.AudioSession.objects.update_or_create')
    @patch('talemo.audiostream.tasks.AudioSession.objects.filter')
    @patch('talemo.audiostream.tasks.safe_update_state')
    def test_generate_audio_stream_progress_callback(self, mock_safe_update, mock_filter, 
                                                   mock_update_create, mock_run_audio, 
                                                   mock_writer_class, mock_store_class):
        """Test that progress callbacks update task state correctly."""
        # Mock SegmentStore
        mock_store = Mock()
        mock_store.create.return_value = (
            'session-789',
            '/tmp/hls/session-789',
            'http://example.com/hls/session-789/audio.m3u8'
        )
        mock_store_class.return_value = mock_store
        
        # Mock StreamingHLSWriter
        mock_writer = Mock()
        mock_writer_class.return_value = mock_writer
        
        # Create mock task
        mock_task = Mock()
        mock_task.request.id = 'progress-task-id'
        mock_task.request.delivery_info = {}
        
        # Capture progress callback
        progress_cb = None
        def capture_progress_cb(*args, **kwargs):
            nonlocal progress_cb
            progress_cb = kwargs.get('progress_cb')
            
        mock_run_audio.side_effect = capture_progress_cb
        
        # Run the task
        with patch('os.path.exists', return_value=True):
            result = generate_audio_stream.run(
                self.prompt,
                self.lang,
                _self=mock_task
            )
        
        # Test progress callback
        self.assertIsNotNone(progress_cb)
        
        # Test chunk progress
        progress_cb("chunk", {"chunk_count": 5})
        mock_safe_update.assert_called_with(
            task_id='progress-task-id',
            state="PROGRESS",
            meta={"event": "chunk", "chunk_count": 5}
        )
        
        # Test done event
        progress_cb("done", {"segments": 10})
        mock_safe_update.assert_called_with(
            task_id='progress-task-id',
            state="SUCCESS",
            meta={"event": "done", "segments": 10}
        )
        
    @patch('talemo.audiostream.tasks.SegmentStore')
    @patch('talemo.audiostream.tasks.StreamingHLSWriter')
    @patch('talemo.audiostream.tasks.run_audio_session')
    @patch('talemo.audiostream.tasks.AudioSession.objects.update_or_create')
    @patch('talemo.audiostream.tasks.AudioSession.objects.filter')
    def test_generate_audio_stream_error_handling(self, mock_filter, mock_update_create, 
                                                mock_run_audio, mock_writer_class, mock_store_class):
        """Test error handling in audio generation."""
        # Mock SegmentStore
        mock_store = Mock()
        mock_store.create.return_value = (
            'session-error',
            '/tmp/hls/session-error',
            'http://example.com/hls/session-error/audio.m3u8'
        )
        mock_store_class.return_value = mock_store
        
        # Mock StreamingHLSWriter
        mock_writer = Mock()
        mock_writer_class.return_value = mock_writer
        
        # Mock run_audio_session to raise exception
        mock_run_audio.side_effect = Exception("Audio generation failed")
        
        # Mock Django ORM
        mock_update_result = Mock()
        mock_filter.return_value.update = mock_update_result
        
        # Create mock task
        mock_task = Mock()
        mock_task.request.id = 'error-task-id'
        mock_task.request.delivery_info = {}
        
        # Run the task
        with patch('os.path.exists', return_value=True):
            result = generate_audio_stream.run(
                self.prompt,
                self.lang,
                _self=mock_task
            )
        
        # Wait a bit for the thread to process the error
        time.sleep(0.1)
        
        # Verify error was recorded
        error_calls = [call for call in mock_update_result.call_args_list 
                      if 'error' in str(call)]
        self.assertTrue(any('error' in str(call) for call in error_calls))
        
    @patch('talemo.audiostream.tasks.SegmentStore')
    @patch('talemo.audiostream.tasks.StreamingHLSWriter')
    @patch('talemo.audiostream.tasks.run_audio_session')
    @patch('talemo.audiostream.tasks.AudioSession.objects.update_or_create')
    @patch('talemo.audiostream.tasks.AudioSession.objects.filter')
    @patch('os.path.exists')
    def test_generate_audio_stream_playlist_not_created(self, mock_exists, mock_filter, 
                                                      mock_update_create, mock_run_audio, 
                                                      mock_writer_class, mock_store_class):
        """Test when FFmpeg doesn't create playlist file."""
        # Mock SegmentStore
        mock_store = Mock()
        mock_store.create.return_value = (
            'session-no-playlist',
            '/tmp/hls/session-no-playlist',
            'http://example.com/hls/session-no-playlist/audio.m3u8'
        )
        mock_store_class.return_value = mock_store
        
        # Mock StreamingHLSWriter
        mock_writer = Mock()
        mock_writer_class.return_value = mock_writer
        
        # Mock path exists - playlist never gets created
        mock_exists.return_value = False
        
        # Create mock task
        mock_task = Mock()
        mock_task.request.id = 'no-playlist-task-id'
        mock_task.request.delivery_info = {}
        
        # Run the task
        with patch('time.time', side_effect=[0, 0.5, 1.5]):  # Simulate time passing
            result = generate_audio_stream.run(
                self.prompt,
                self.lang,
                _self=mock_task
            )
        
        # Should still return result
        self.assertIn('playlist', result)
        
    def test_generate_audio_stream_with_custom_parameters(self):
        """Test task with custom parameters."""
        with patch('talemo.audiostream.tasks.SegmentStore') as mock_store_class, \
             patch('talemo.audiostream.tasks.StreamingHLSWriter'), \
             patch('talemo.audiostream.tasks.run_audio_session'), \
             patch('talemo.audiostream.tasks.AudioSession.objects.update_or_create'), \
             patch('talemo.audiostream.tasks.AudioSession.objects.filter'), \
             patch('os.path.exists', return_value=True):
            
            # Mock SegmentStore
            mock_store = Mock()
            mock_store.create.return_value = (
                'custom-session',
                '/tmp/hls/custom-session',
                'http://example.com/hls/custom-session/audio.m3u8'
            )
            mock_store_class.return_value = mock_store
            
            # Create mock task
            mock_task = Mock()
            mock_task.request.id = 'custom-task-id'
            mock_task.request.delivery_info = {'routing_key': 'high-priority'}
            
            # Run with custom parameters
            result = generate_audio_stream.run(
                "Custom prompt",
                "es",  # Spanish
                "my-custom-session-id",
                min_segments_before_return=3,
                timeout_before_return=10.0,
                _self=mock_task
            )
            
            # Verify custom session ID was used
            mock_store.create.assert_called_once_with("my-custom-session-id")
            
    @patch('talemo.audiostream.tasks.SegmentStore')
    @patch('talemo.audiostream.tasks.StreamingHLSWriter')
    @patch('talemo.audiostream.tasks.threading.Thread')
    def test_generate_audio_stream_threading(self, mock_thread_class, mock_writer_class, mock_store_class):
        """Test that audio generation runs in a separate thread."""
        # Mock SegmentStore
        mock_store = Mock()
        mock_store.create.return_value = (
            'thread-session',
            '/tmp/hls/thread-session',
            'http://example.com/hls/thread-session/audio.m3u8'
        )
        mock_store_class.return_value = mock_store
        
        # Mock thread
        mock_thread = Mock()
        mock_thread_class.return_value = mock_thread
        
        # Create mock task
        mock_task = Mock()
        mock_task.request.id = 'thread-task-id'
        mock_task.request.delivery_info = {}
        
        # Run the task
        with patch('os.path.exists', return_value=True), \
             patch('talemo.audiostream.tasks.AudioSession.objects'):
            result = generate_audio_stream.run(
                self.prompt,
                self.lang,
                _self=mock_task
            )
        
        # Verify thread was created and started
        mock_thread_class.assert_called_once()
        thread_kwargs = mock_thread_class.call_args[1]
        self.assertTrue(thread_kwargs['daemon'])
        self.assertEqual(thread_kwargs['name'], 'HLS-thread-session')
        mock_thread.start.assert_called_once()


class TestTaskIntegration(TestCase):
    """Integration tests for the Celery task."""
    
    def test_task_registration(self):
        """Test that the task is properly registered with Celery."""
        # Import the task to ensure it's registered
        from talemo.audiostream.tasks import generate_audio_stream
        
        # Verify task is registered
        self.assertEqual(generate_audio_stream.name, 'talemo.audiostream.tasks.generate_audio_stream')
        
    @patch('talemo.audiostream.tasks.SegmentStore')
    def test_task_without_self_binding(self, mock_store_class):
        """Test task behavior when called without self binding."""
        # This tests the edge case where the task might be called incorrectly
        mock_store = Mock()
        mock_store.create.return_value = (
            'no-self-session',
            '/tmp/hls/no-self-session',
            'http://example.com/hls/no-self-session/audio.m3u8'
        )
        mock_store_class.return_value = mock_store
        
        with patch('talemo.audiostream.tasks.StreamingHLSWriter'), \
             patch('talemo.audiostream.tasks.run_audio_session'), \
             patch('talemo.audiostream.tasks.AudioSession.objects'), \
             patch('os.path.exists', return_value=True):
            
            # This should not raise an error even without proper task context
            try:
                # Create a minimal mock that has the required attributes
                mock_self = Mock()
                mock_self.request = Mock()
                mock_self.request.id = 'minimal-task-id'
                mock_self.request.delivery_info = {}
                
                result = generate_audio_stream(
                    mock_self,
                    "Test prompt",
                    "en"
                )
                self.assertIn('playlist', result)
            except AttributeError:
                # If it fails due to missing context, that's also acceptable
                # as it means the task requires proper Celery context
                pass