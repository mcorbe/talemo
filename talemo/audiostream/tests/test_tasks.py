from unittest import mock
from django.test import TestCase, override_settings

# Mock the OpenAI client before importing any modules that use it
mock.patch('openai.AsyncOpenAI').start()

from talemo.audiostream.tasks import generate_audio_stream
from talemo.audiostream.models import AudioSession

class TasksTestCase(TestCase):

    @mock.patch('talemo.audiostream.tasks.run_audio_session')
    @mock.patch('talemo.audiostream.tasks.SegmentStore')
    def test_generate_audio_stream(self, mock_segment_store, mock_run_audio_session):
        # Mock the run_audio_session function to avoid actual API calls and ffmpeg processing
        mock_run_audio_session.return_value = {"chunk_count": 2}

        # Mock the SegmentStore
        mock_store = mock_segment_store.return_value
        mock_store.create.return_value = ("test_session_id", "/tmp/test_path", "/media/hls/test_session_id/audio.m3u8")

        # Call the task function directly instead of using delay()
        result = generate_audio_stream("Test prompt", "en")

        # Verify that an AudioSession was created with the correct status
        session = AudioSession.objects.filter(session_id="test_session_id").first()
        self.assertIsNotNone(session)
        self.assertEqual(session.status, "ready")
        self.assertNotEqual(session.playlist_rel_url, "")

        # Verify that run_audio_session was called with the correct arguments
        mock_run_audio_session.assert_called_once()
        args, kwargs = mock_run_audio_session.call_args
        self.assertEqual(args[0], "Test prompt")  # First arg should be the prompt
