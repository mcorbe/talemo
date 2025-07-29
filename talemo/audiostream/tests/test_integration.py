import os
import time
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from talemo.audiostream.models import AudioSession
from talemo.audiostream.tasks import generate_audio_stream


class TestAudioStreamingIntegration(TransactionTestCase):
    """Integration tests for the complete audio streaming flow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            
    @patch('talemo.audiostream.tasks.SegmentStore')
    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.tts.speak_chunk_to_ffmpeg')
    @patch('talemo.audiostream.views.redis.Redis.from_url')
    def test_complete_audio_generation_flow(self, mock_redis_from_url, mock_speak, 
                                          mock_stream_tokens, mock_writer_class, mock_store_class):
        """Test the complete flow from API request to audio generation."""
        # Mock Redis availability
        mock_redis_client = Mock()
        mock_redis_client.ping.return_value = True
        mock_redis_from_url.return_value = mock_redis_client
        
        # Mock SegmentStore
        session_id = 'integration-test-session'
        hls_path = os.path.join(self.temp_dir, session_id)
        playlist_url = f'http://testserver/hls/{session_id}/audio.m3u8'
        
        mock_store = Mock()
        mock_store.create.return_value = (session_id, hls_path, playlist_url)
        mock_store_class.return_value = mock_store
        
        # Mock StreamingHLSWriter
        mock_writer = Mock()
        mock_writer.ffmpeg_process = Mock()
        mock_writer.ffmpeg_process.poll.return_value = None
        mock_writer.ffmpeg_stdin = Mock()
        mock_writer.ffmpeg_stdin.closed = False
        mock_writer.finalize.return_value = {'chunks': 3, 'segment_count': 3}
        mock_writer_class.return_value = mock_writer
        
        # Mock LLM tokens
        async def mock_token_generator():
            tokens = ["This", " ", "is", " ", "a", " ", "test", ".", " ", "Hello", "!"]
            for token in tokens:
                yield token
                
        mock_stream_tokens.return_value = mock_token_generator()
        
        # Create the HLS directory
        os.makedirs(hls_path, exist_ok=True)
        
        # Step 1: Start audio session via API
        with self.settings(CELERY_TASK_ALWAYS_EAGER=True, HLS_URL='http://testserver/hls/'):
            response = self.client.post(
                reverse('audiostream:start_session'),
                {'prompt': 'Generate test audio', 'lang': 'en'},
                format='json'
            )
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('session_id', response.data)
        self.assertIn('playlist', response.data)
        self.assertIn('task_id', response.data)
        
        # Step 2: Verify AudioSession was created
        audio_session = AudioSession.objects.filter(session_id=session_id).first()
        self.assertIsNotNone(audio_session)
        self.assertEqual(audio_session.status, 'ready')
        
        # Step 3: Verify audio generation was triggered
        mock_stream_tokens.assert_called()
        mock_speak.assert_called()
        
        # Step 4: Check task status
        task_id = response.data['task_id']
        status_response = self.client.get(
            reverse('audiostream:task_status', args=[task_id])
        )
        
        # In CELERY_TASK_ALWAYS_EAGER mode, task completes synchronously
        self.assertEqual(status_response.status_code, status.HTTP_200_OK)
        
    @patch('talemo.audiostream.views.generate_audio_stream.delay')
    @patch('talemo.audiostream.views.redis.Redis.from_url')
    @patch('celery.result.AsyncResult')
    def test_async_task_status_progression(self, mock_async_result_class, 
                                          mock_redis_from_url, mock_task_delay):
        """Test async task status progression from pending to success."""
        # Mock Redis
        mock_redis_client = Mock()
        mock_redis_client.ping.return_value = True
        mock_redis_from_url.return_value = mock_redis_client
        
        # Mock task creation
        mock_async_result = Mock()
        mock_async_result.ready.return_value = False
        mock_async_result.id = 'progress-test-task'
        mock_task_delay.return_value = mock_async_result
        
        # Start session
        with self.settings(CELERY_TASK_ALWAYS_EAGER=False, HLS_URL='http://testserver/hls/'):
            start_response = self.client.post(
                reverse('audiostream:start_session'),
                {'prompt': 'Test async flow', 'lang': 'en'},
                format='json'
            )
        
        self.assertEqual(start_response.status_code, status.HTTP_200_OK)
        task_id = start_response.data['task_id']
        
        # Simulate task progression
        status_url = reverse('audiostream:task_status', args=[task_id])
        
        # Stage 1: PENDING
        mock_result = Mock()
        mock_result.state = 'PENDING'
        mock_async_result_class.return_value = mock_result
        
        response = self.client.get(status_url)
        self.assertEqual(response.data['state'], 'PENDING')
        
        # Stage 2: PROGRESS
        mock_result.state = 'PROGRESS'
        mock_result.info = {'event': 'chunk', 'chunk_count': 2}
        
        response = self.client.get(status_url)
        self.assertEqual(response.data['state'], 'PROGRESS')
        self.assertEqual(response.data['chunk_count'], 2)
        
        # Stage 3: SUCCESS
        mock_result.state = 'SUCCESS'
        mock_result.get.return_value = {
            'playlist': 'http://testserver/hls/test-session/audio.m3u8'
        }
        
        response = self.client.get(status_url)
        self.assertEqual(response.data['state'], 'SUCCESS')
        self.assertIn('playlist', response.data)
        
    @patch('talemo.audiostream.tasks.SegmentStore')
    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.tts.speak_chunk_to_ffmpeg')
    def test_error_handling_in_pipeline(self, mock_speak, mock_stream_tokens, 
                                       mock_writer_class, mock_store_class):
        """Test error handling throughout the pipeline."""
        # Mock SegmentStore
        session_id = 'error-test-session'
        mock_store = Mock()
        mock_store.create.return_value = (
            session_id,
            os.path.join(self.temp_dir, session_id),
            f'http://testserver/hls/{session_id}/audio.m3u8'
        )
        mock_store_class.return_value = mock_store
        
        # Mock LLM to raise error
        async def mock_error_generator():
            raise Exception("LLM service error")
            yield  # Make it a generator
            
        mock_stream_tokens.return_value = mock_error_generator()
        
        # Mock HLS writer
        mock_writer = Mock()
        mock_writer.finalize.return_value = {'chunks': 0, 'segment_count': 0}
        mock_writer_class.return_value = mock_writer
        
        # Start session with synchronous execution
        with self.settings(CELERY_TASK_ALWAYS_EAGER=True, HLS_URL='http://testserver/hls/'):
            response = self.client.post(
                reverse('audiostream:start_session'),
                {'prompt': 'This will fail', 'lang': 'en'},
                format='json'
            )
        
        # Should still return success (task queued)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that AudioSession reflects error state
        time.sleep(0.1)  # Give time for error handling
        audio_session = AudioSession.objects.filter(session_id=session_id).first()
        # Session should exist even if there was an error
        self.assertIsNotNone(audio_session)
        
    def test_concurrent_sessions(self):
        """Test handling multiple concurrent audio sessions."""
        with patch('talemo.audiostream.views.generate_audio_stream.delay') as mock_task_delay, \
             patch('talemo.audiostream.views.redis.Redis.from_url') as mock_redis_from_url:
            
            # Mock Redis
            mock_redis_client = Mock()
            mock_redis_client.ping.return_value = True
            mock_redis_from_url.return_value = mock_redis_client
            
            # Mock different task results
            mock_results = []
            for i in range(3):
                mock_result = Mock()
                mock_result.ready.return_value = False
                mock_result.id = f'concurrent-task-{i}'
                mock_results.append(mock_result)
                
            mock_task_delay.side_effect = mock_results
            
            # Start multiple sessions
            sessions = []
            with self.settings(CELERY_TASK_ALWAYS_EAGER=False, HLS_URL='http://testserver/hls/'):
                for i in range(3):
                    response = self.client.post(
                        reverse('audiostream:start_session'),
                        {'prompt': f'Concurrent test {i}', 'lang': 'en'},
                        format='json'
                    )
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                    sessions.append(response.data)
            
            # Verify all sessions have unique IDs
            session_ids = [s['session_id'] for s in sessions]
            self.assertEqual(len(set(session_ids)), 3)
            
            # Verify all tasks were queued
            self.assertEqual(mock_task_delay.call_count, 3)
            
    @patch('talemo.audiostream.pipeline.os.path.join')
    @patch('talemo.audiostream.pipeline.open', create=True)
    @patch('talemo.audiostream.tasks.SegmentStore')
    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.tts.speak_chunk_to_ffmpeg')
    def test_text_logging_integration(self, mock_speak, mock_stream_tokens, mock_writer_class,
                                    mock_store_class, mock_open, mock_path_join):
        """Test that text chunks are properly logged during generation."""
        # Mock SegmentStore
        session_id = 'logging-test-session'
        hls_path = os.path.join(self.temp_dir, session_id)
        
        mock_store = Mock()
        mock_store.create.return_value = (
            session_id,
            hls_path,
            f'http://testserver/hls/{session_id}/audio.m3u8'
        )
        mock_store_class.return_value = mock_store
        
        # Mock path.join to return expected paths
        def path_join_side_effect(*args):
            return os.path.join(*args)
        mock_path_join.side_effect = path_join_side_effect
        
        # Mock file operations
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Mock HLS writer
        mock_writer = Mock()
        mock_writer.ffmpeg_process = Mock()
        mock_writer.ffmpeg_process.poll.return_value = None
        mock_writer.ffmpeg_stdin = Mock()
        mock_writer.ffmpeg_stdin.closed = False
        mock_writer.finalize.return_value = {'chunks': 2, 'segment_count': 2}
        mock_writer_class.return_value = mock_writer
        
        # Mock LLM tokens
        async def mock_token_generator():
            yield "First chunk."
            yield " Second chunk!"
            
        mock_stream_tokens.return_value = mock_token_generator()
        
        # Run with synchronous execution
        with self.settings(CELERY_TASK_ALWAYS_EAGER=True, HLS_URL='http://testserver/hls/'):
            response = self.client.post(
                reverse('audiostream:start_session'),
                {'prompt': 'Test logging', 'lang': 'en'},
                format='json'
            )
        
        # Verify text log file was created and written to
        self.assertTrue(mock_open.called)
        
        # Check that chunk text was logged
        write_calls = mock_file.write.call_args_list
        logged_text = ''.join([call[0][0] for call in write_calls])
        self.assertIn('Audio Generation Session', logged_text)
        self.assertIn('Test logging', logged_text)  # Original prompt
        
    def test_invalid_request_handling(self):
        """Test handling of invalid API requests."""
        # Test missing prompt
        response = self.client.post(
            reverse('audiostream:start_session'),
            {'lang': 'en'},  # Missing prompt
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Test invalid task status
        response = self.client.get(
            reverse('audiostream:task_status', args=['invalid-task-id'])
        )
        # Should still return 200 with task state
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    @patch('talemo.audiostream.views.generate_audio_stream')
    def test_sync_fallback_integration(self, mock_task_func):
        """Test fallback to synchronous execution when async not available."""
        # Mock synchronous task execution
        mock_task_func.return_value = {
            'playlist': 'http://testserver/hls/sync-session/audio.m3u8'
        }
        
        # Disable Redis to force sync mode
        with self.settings(CELERY_TASK_ALWAYS_EAGER=True, HLS_URL='http://testserver/hls/'):
            response = self.client.post(
                reverse('audiostream:start_session'),
                {'prompt': 'Sync fallback test', 'lang': 'fr'},
                format='json'
            )
        
        # Verify request succeeded
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('playlist', response.data)
        
        # Verify sync function was called directly
        mock_task_func.assert_called_once()
        call_args = mock_task_func.call_args[0]
        self.assertEqual(call_args[0], 'Sync fallback test')
        self.assertEqual(call_args[1], 'fr')


class TestEndToEndScenarios(TestCase):
    """Test real-world usage scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        
    @patch('talemo.audiostream.views.generate_audio_stream.delay')
    @patch('talemo.audiostream.views.redis.Redis.from_url')
    def test_user_workflow_generate_and_check(self, mock_redis_from_url, mock_task_delay):
        """Test typical user workflow: generate audio and check status."""
        # Mock Redis
        mock_redis_client = Mock()
        mock_redis_client.ping.return_value = True
        mock_redis_from_url.return_value = mock_redis_client
        
        # Mock task
        mock_async_result = Mock()
        mock_async_result.ready.return_value = False
        mock_async_result.id = 'user-workflow-task'
        mock_task_delay.return_value = mock_async_result
        
        # User starts audio generation
        with self.settings(CELERY_TASK_ALWAYS_EAGER=False, HLS_URL='http://testserver/hls/'):
            start_response = self.client.post(
                reverse('audiostream:start_session'),
                {
                    'prompt': 'Tell me a story about a brave knight',
                    'lang': 'en'
                },
                format='json'
            )
        
        # User gets response with playlist URL
        self.assertEqual(start_response.status_code, status.HTTP_200_OK)
        playlist_url = start_response.data['playlist']
        task_id = start_response.data['task_id']
        
        # User checks task status periodically
        with patch('celery.result.AsyncResult') as mock_async_result_class:
            # First check - still processing
            mock_result = Mock()
            mock_result.state = 'PROGRESS'
            mock_result.info = {'event': 'chunk', 'chunk_count': 5}
            mock_async_result_class.return_value = mock_result
            
            status_response = self.client.get(
                reverse('audiostream:task_status', args=[task_id])
            )
            self.assertEqual(status_response.data['state'], 'PROGRESS')
            
            # Second check - completed
            mock_result.state = 'SUCCESS'
            mock_result.get.return_value = {'playlist': playlist_url}
            
            status_response = self.client.get(
                reverse('audiostream:task_status', args=[task_id])
            )
            self.assertEqual(status_response.data['state'], 'SUCCESS')
            
        # User would then use the playlist URL to stream audio
        self.assertIn('http://testserver/hls/', playlist_url)
        
    def test_multilingual_support(self):
        """Test audio generation in different languages."""
        languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'zh']
        
        with patch('talemo.audiostream.views.generate_audio_stream') as mock_task_func:
            mock_task_func.return_value = {'playlist': 'http://test.com/audio.m3u8'}
            
            with self.settings(CELERY_TASK_ALWAYS_EAGER=True):
                for lang in languages:
                    response = self.client.post(
                        reverse('audiostream:start_session'),
                        {
                            'prompt': f'Test in {lang}',
                            'lang': lang
                        },
                        format='json'
                    )
                    
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                    
                    # Verify language was passed correctly
                    call_args = mock_task_func.call_args[0]
                    self.assertEqual(call_args[1], lang)