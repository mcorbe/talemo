from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest import mock
from rest_framework.test import APIClient
import os
import time
import requests
import tempfile
import shutil

# Mock the OpenAI client before importing any modules that use it
mock.patch('openai.AsyncOpenAI').start()

# Now it's safe to import the view
from talemo.audiostream.views import start_audio_session
from talemo.audiostream.models import AudioSession

class AudioStreamViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    @mock.patch('talemo.audiostream.views.generate_audio_stream')
    def test_start_audio_session(self, mock_generate_audio_stream):
        # Mock the Celery task
        mock_async_result = mock.MagicMock()
        mock_async_result.id = 'test_task_id'
        mock_generate_audio_stream.delay.return_value = mock_async_result

        # Create a test client and authenticate
        client = APIClient()
        client.force_authenticate(user=self.user)

        # Make a POST request to the endpoint
        url = reverse('start-audio')
        data = {'prompt': 'This is a test prompt for audio streaming.'}
        response = client.post(url, data=data, content_type='application/json')

        # Check if the request was successful
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response
        response_data = response.json()

        # Check if the response contains a playlist URL
        self.assertIn('playlist', response_data)

        # Verify the URL format
        self.assertIn('/media/hls/', response_data['playlist'])
        self.assertTrue(response_data['playlist'].endswith('/audio.m3u8'))

        # Check if the session_id is correct
        self.assertEqual(response_data['session_id'], 'test_task_id')

        # Print the response for manual verification
        print(f"Response: {response_data}")

    @mock.patch('talemo.audiostream.tasks.run_audio_session')
    def test_playlist_bootstrap_logic(self, mock_run_audio_session):
        """
        Test that the playlist is created early and contains at least one #EXTINF entry.
        This test verifies the bootstrap logic that allows playback to start before
        the entire audio is generated.
        """
        # Create a temporary directory for the test
        test_dir = tempfile.mkdtemp()
        try:
            # Create a mock implementation of run_audio_session that:
            # 1. Creates a valid playlist file with at least one segment
            # 2. Simulates the background processing
            def mock_audio_session_impl(prompt, playlist_path, lang, progress_cb=None):
                # Create the directory structure
                os.makedirs(os.path.dirname(playlist_path), exist_ok=True)

                # Create a minimal valid playlist with one segment
                with open(playlist_path, 'w') as f:
                    f.write("#EXTM3U\n")
                    f.write("#EXT-X-VERSION:7\n")
                    f.write("#EXT-X-TARGETDURATION:2\n")
                    f.write("#EXT-X-MEDIA-SEQUENCE:0\n")
                    f.write("#EXT-X-PLAYLIST-TYPE:EVENT\n")
                    f.write("#EXTINF:2.0,\n")  # Add a segment entry
                    f.write("segment_000.m4s\n")

                # Create a dummy segment file
                segment_path = os.path.join(os.path.dirname(playlist_path), "segment_000.m4s")
                with open(segment_path, 'wb') as f:
                    f.write(b'dummy segment data')

                # Call the progress callback if provided
                if progress_cb:
                    progress_cb("chunk", {"chunk_count": 1})

                # Return success
                return {"playlist_path": playlist_path, "segment_count": 1}

            # Set up the mock
            mock_run_audio_session.side_effect = mock_audio_session_impl

            # Create a test client and authenticate
            client = APIClient()
            client.force_authenticate(user=self.user)

            # Make a POST request to the endpoint
            url = reverse('start-audio')
            data = {'prompt': 'Test prompt for bootstrap logic.'}
            response = client.post(url, data=data, content_type='application/json')

            # Check if the request was successful
            self.assertEqual(response.status_code, 200)

            # Parse the JSON response
            response_data = response.json()

            # Check if the response contains a playlist URL
            self.assertIn('playlist', response_data)
            playlist_url = response_data['playlist']

            # Get the session ID
            session_id = response_data.get('session_id') or response_data.get('task_id')
            self.assertIsNotNone(session_id)

            # Wait a short time for the playlist to be populated
            time.sleep(1)

            # Get the session from the database
            session = AudioSession.objects.get(session_id=session_id)

            # Get the actual file path from the database
            playlist_rel_url = session.playlist_rel_url

            # Construct the absolute path to the playlist file
            from django.conf import settings
            media_root = settings.MEDIA_ROOT
            playlist_path = os.path.join(media_root, playlist_rel_url.lstrip('/media/'))

            # Verify the playlist file exists
            self.assertTrue(os.path.exists(playlist_path), f"Playlist file does not exist at {playlist_path}")

            # Read the playlist file and check for #EXTINF
            with open(playlist_path, 'r') as f:
                playlist_content = f.read()

            # Assert that the playlist contains at least one #EXTINF entry
            self.assertIn('#EXTINF', playlist_content, 
                         f"Playlist does not contain any #EXTINF entries. Content: {playlist_content}")

            print(f"Playlist content: {playlist_content}")

        finally:
            # Clean up the temporary directory
            shutil.rmtree(test_dir, ignore_errors=True)
