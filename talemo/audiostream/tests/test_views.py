import uuid
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from talemo.audiostream.views import start_audio_session, task_status


class TestStartAudioSessionView(TestCase):
    """Test cases for the start_audio_session API endpoint."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        self.url = reverse('audiostream:start_session')  # Adjust based on your URL conf
        
    @patch('talemo.audiostream.views.generate_audio_stream.delay')
    @patch('talemo.audiostream.views.redis.Redis.from_url')
    def test_start_audio_session_async_success(self, mock_redis_from_url, mock_task_delay):
        """Test successful async audio session creation."""
        # Mock Redis connection
        mock_redis_client = Mock()
        mock_redis_client.ping.return_value = True
        mock_redis_from_url.return_value = mock_redis_client
        
        # Mock Celery task
        mock_async_result = Mock()
        mock_async_result.ready.return_value = False
        mock_async_result.id = 'test-task-id'
        mock_task_delay.return_value = mock_async_result
        
        # Make request
        data = {
            'prompt': 'Test prompt for audio generation',
            'lang': 'en'
        }
        
        with self.settings(CELERY_TASK_ALWAYS_EAGER=False, HLS_URL='http://example.com/hls/'):
            response = self.client.post(self.url, data, format='json')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('session_id', response.data)
        self.assertIn('playlist', response.data)
        self.assertIn('task_id', response.data)
        
        # Verify task was called
        mock_task_delay.assert_called_once()
        call_args = mock_task_delay.call_args[0]
        self.assertEqual(call_args[0], 'Test prompt for audio generation')
        self.assertEqual(call_args[1], 'en')
        
    @patch('talemo.audiostream.views.generate_audio_stream.delay')
    @patch('talemo.audiostream.views.redis.Redis.from_url')
    def test_start_audio_session_async_with_ready_result(self, mock_redis_from_url, mock_task_delay):
        """Test async session when task result is immediately ready."""
        # Mock Redis connection
        mock_redis_client = Mock()
        mock_redis_client.ping.return_value = True
        mock_redis_from_url.return_value = mock_redis_client
        
        # Mock Celery task that's already ready
        mock_async_result = Mock()
        mock_async_result.ready.return_value = True
        mock_async_result.get.return_value = {
            'playlist': 'http://example.com/custom-playlist.m3u8'
        }
        mock_task_delay.return_value = mock_async_result
        
        # Make request
        data = {'prompt': 'Quick test', 'lang': 'es'}
        
        with self.settings(CELERY_TASK_ALWAYS_EAGER=False, HLS_URL='http://example.com/hls/'):
            response = self.client.post(self.url, data, format='json')
        
        # Should use the playlist from task result
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['playlist'], 'http://example.com/custom-playlist.m3u8')
        
    @patch('talemo.audiostream.views.generate_audio_stream')
    @patch('talemo.audiostream.views.redis.Redis.from_url')
    def test_start_audio_session_sync_mode(self, mock_redis_from_url, mock_task_func):
        """Test synchronous execution when CELERY_TASK_ALWAYS_EAGER is True."""
        # Mock Redis connection
        mock_redis_client = Mock()
        mock_redis_client.ping.return_value = True
        mock_redis_from_url.return_value = mock_redis_client
        
        # Mock synchronous task execution
        mock_task_func.return_value = {
            'playlist': 'http://example.com/sync-playlist.m3u8'
        }
        
        # Make request
        data = {'prompt': 'Sync test', 'lang': 'fr'}
        
        with self.settings(CELERY_TASK_ALWAYS_EAGER=True, HLS_URL='http://example.com/hls/'):
            response = self.client.post(self.url, data, format='json')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('session_id', response.data)
        self.assertIn('playlist', response.data)
        
        # Verify synchronous task was called
        mock_task_func.assert_called_once()
        
    @patch('talemo.audiostream.views.generate_audio_stream')
    @patch('talemo.audiostream.views.redis.Redis.from_url')
    def test_start_audio_session_redis_unavailable(self, mock_redis_from_url, mock_task_func):
        """Test fallback to sync when Redis is unavailable."""
        # Mock Redis connection failure
        mock_redis_client = Mock()
        mock_redis_client.ping.side_effect = Exception("Redis connection error")
        mock_redis_from_url.return_value = mock_redis_client
        
        # Mock synchronous task execution
        mock_task_func.return_value = {'status': 'ok'}
        
        # Make request
        data = {'prompt': 'Redis down test'}
        
        with self.settings(CELERY_TASK_ALWAYS_EAGER=False, HLS_URL='http://example.com/hls/'):
            response = self.client.post(self.url, data, format='json')
        
        # Should fall back to sync execution
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_task_func.assert_called_once()
        
    @patch('talemo.audiostream.views.generate_audio_stream')
    def test_start_audio_session_sync_task_error(self, mock_task_func):
        """Test error handling in synchronous task execution."""
        # Mock task failure
        mock_task_func.side_effect = Exception("Task execution error")
        
        # Make request
        data = {'prompt': 'Error test'}
        
        with self.settings(CELERY_TASK_ALWAYS_EAGER=True, HLS_URL='http://example.com/hls/'):
            response = self.client.post(self.url, data, format='json')
        
        # Should return error response
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "Task execution error")
        
    def test_start_audio_session_missing_prompt(self):
        """Test request without required prompt field."""
        data = {'lang': 'en'}  # Missing prompt
        
        with self.assertRaises(KeyError):
            response = self.client.post(self.url, data, format='json')
            
    @patch('talemo.audiostream.views.generate_audio_stream.delay')
    @patch('talemo.audiostream.views.redis.Redis.from_url')
    def test_start_audio_session_default_language(self, mock_redis_from_url, mock_task_delay):
        """Test that default language is used when not specified."""
        # Mock Redis
        mock_redis_client = Mock()
        mock_redis_client.ping.return_value = True
        mock_redis_from_url.return_value = mock_redis_client
        
        # Mock Celery task
        mock_async_result = Mock()
        mock_async_result.ready.return_value = False
        mock_task_delay.return_value = mock_async_result
        
        # Make request without language
        data = {'prompt': 'Test without language'}
        
        with self.settings(CELERY_TASK_ALWAYS_EAGER=False, HLS_URL='http://example.com/hls/'):
            response = self.client.post(self.url, data, format='json')
        
        # Verify default language 'en' was used
        call_args = mock_task_delay.call_args[0]
        self.assertEqual(call_args[1], 'en')
        
    @patch('talemo.audiostream.views.generate_audio_stream.delay')
    @patch('talemo.audiostream.views.redis.Redis.from_url')
    def test_start_audio_session_celery_delay_error(self, mock_redis_from_url, mock_task_delay):
        """Test fallback when Celery delay() fails."""
        # Mock Redis available
        mock_redis_client = Mock()
        mock_redis_client.ping.return_value = True
        mock_redis_from_url.return_value = mock_redis_client
        
        # Mock Celery delay failure
        mock_task_delay.side_effect = Exception("Celery broker error")
        
        # Mock synchronous execution
        with patch('talemo.audiostream.views.generate_audio_stream') as mock_sync_task:
            mock_sync_task.return_value = {'status': 'ok'}
            
            # Make request
            data = {'prompt': 'Celery error test'}
            
            with self.settings(CELERY_TASK_ALWAYS_EAGER=False, HLS_URL='http://example.com/hls/'):
                response = self.client.post(self.url, data, format='json')
            
            # Should fall back to sync
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            mock_sync_task.assert_called_once()


class TestTaskStatusView(TestCase):
    """Test cases for the task_status API endpoint."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        
    def get_url(self, task_id):
        """Helper to get the task status URL."""
        return reverse('audiostream:task_status', args=[task_id])
        
    @patch('talemo.audiostream.views.AsyncResult')
    def test_task_status_pending(self, mock_async_result_class):
        """Test status check for pending task."""
        # Mock AsyncResult
        mock_result = Mock()
        mock_result.state = 'PENDING'
        mock_async_result_class.return_value = mock_result
        
        # Make request
        task_id = 'test-task-123'
        response = self.client.get(self.get_url(task_id))
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 'PENDING')
        self.assertEqual(response.data['status'], 'Task is pending')
        
    @patch('talemo.audiostream.views.AsyncResult')
    def test_task_status_progress(self, mock_async_result_class):
        """Test status check for task in progress."""
        # Mock AsyncResult with progress info
        mock_result = Mock()
        mock_result.state = 'PROGRESS'
        mock_result.info = {
            'event': 'chunk',
            'chunk_count': 5,
            'total_chunks': 10
        }
        mock_async_result_class.return_value = mock_result
        
        # Make request
        response = self.client.get(self.get_url('progress-task'))
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 'PROGRESS')
        self.assertEqual(response.data['status'], 'Task is in progress')
        self.assertEqual(response.data['event'], 'chunk')
        self.assertEqual(response.data['chunk_count'], 5)
        self.assertEqual(response.data['total_chunks'], 10)
        
    @patch('talemo.audiostream.views.AsyncResult')
    def test_task_status_success(self, mock_async_result_class):
        """Test status check for successful task."""
        # Mock AsyncResult with success
        mock_result = Mock()
        mock_result.state = 'SUCCESS'
        mock_result.get.return_value = {
            'playlist': 'http://example.com/success.m3u8',
            'segments': 15
        }
        mock_async_result_class.return_value = mock_result
        
        # Make request
        response = self.client.get(self.get_url('success-task'))
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 'SUCCESS')
        self.assertEqual(response.data['status'], 'Task completed successfully')
        self.assertEqual(response.data['playlist'], 'http://example.com/success.m3u8')
        self.assertEqual(response.data['result']['segments'], 15)
        
    @patch('talemo.audiostream.views.AsyncResult')
    def test_task_status_failure(self, mock_async_result_class):
        """Test status check for failed task."""
        # Mock AsyncResult with failure
        mock_result = Mock()
        mock_result.state = 'FAILURE'
        mock_result.result = Exception("Audio generation failed")
        mock_async_result_class.return_value = mock_result
        
        # Make request
        response = self.client.get(self.get_url('failed-task'))
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 'FAILURE')
        self.assertEqual(response.data['status'], 'Task failed')
        self.assertIn('Audio generation failed', response.data['error'])
        
    @patch('talemo.audiostream.views.AsyncResult')
    def test_task_status_unknown_state(self, mock_async_result_class):
        """Test status check for unknown task state."""
        # Mock AsyncResult with unknown state
        mock_result = Mock()
        mock_result.state = 'CUSTOM_STATE'
        mock_async_result_class.return_value = mock_result
        
        # Make request
        response = self.client.get(self.get_url('unknown-task'))
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 'CUSTOM_STATE')
        self.assertEqual(response.data['status'], 'Unknown state: CUSTOM_STATE')
        
    @patch('talemo.audiostream.views.AsyncResult')
    def test_task_status_progress_without_info(self, mock_async_result_class):
        """Test progress state without meta information."""
        # Mock AsyncResult with progress but no info
        mock_result = Mock()
        mock_result.state = 'PROGRESS'
        mock_result.info = None
        mock_async_result_class.return_value = mock_result
        
        # Make request
        response = self.client.get(self.get_url('progress-no-info'))
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 'PROGRESS')
        self.assertEqual(response.data['status'], 'Task is in progress')
        # Should not have additional fields
        self.assertNotIn('event', response.data)


class TestViewsIntegration(TestCase):
    """Integration tests for views working together."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        
    @patch('talemo.audiostream.views.generate_audio_stream.delay')
    @patch('talemo.audiostream.views.redis.Redis.from_url')
    @patch('talemo.audiostream.views.AsyncResult')
    def test_start_session_and_check_status(self, mock_async_result_class, mock_redis_from_url, mock_task_delay):
        """Test creating a session and then checking its status."""
        # Mock Redis
        mock_redis_client = Mock()
        mock_redis_client.ping.return_value = True
        mock_redis_from_url.return_value = mock_redis_client
        
        # Mock task creation
        mock_async_result = Mock()
        mock_async_result.ready.return_value = False
        mock_async_result.id = 'integration-test-id'
        mock_task_delay.return_value = mock_async_result
        
        # Start session
        start_url = reverse('audiostream:start_session')
        data = {'prompt': 'Integration test prompt', 'lang': 'en'}
        
        with self.settings(CELERY_TASK_ALWAYS_EAGER=False, HLS_URL='http://example.com/hls/'):
            start_response = self.client.post(start_url, data, format='json')
        
        self.assertEqual(start_response.status_code, status.HTTP_200_OK)
        session_id = start_response.data['session_id']
        task_id = start_response.data['task_id']
        
        # Mock task status check
        mock_status_result = Mock()
        mock_status_result.state = 'PROGRESS'
        mock_status_result.info = {'event': 'chunk', 'chunk_count': 3}
        mock_async_result_class.return_value = mock_status_result
        
        # Check status
        status_url = reverse('audiostream:task_status', args=[task_id])
        status_response = self.client.get(status_url)
        
        self.assertEqual(status_response.status_code, status.HTTP_200_OK)
        self.assertEqual(status_response.data['state'], 'PROGRESS')
        self.assertEqual(status_response.data['chunk_count'], 3)