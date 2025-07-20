from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest import mock
from rest_framework.test import APIClient

# Mock the OpenAI client before importing any modules that use it
mock.patch('openai.AsyncOpenAI').start()

# Now it's safe to import the view
from talemo.audiostream.views import start_audio_session

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
