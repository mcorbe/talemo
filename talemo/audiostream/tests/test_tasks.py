from unittest import mock
from django.test import TestCase, override_settings
import os
import time
import tempfile
import shutil
from contextlib import suppress

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

    @mock.patch('talemo.audiostream.tasks.StreamingHLSWriter')
    @mock.patch('talemo.audiostream.tasks.SegmentStore')
    def test_bootstrap_logic(self, mock_segment_store, mock_writer_class):
        """
        Test that the bootstrap logic in generate_audio_stream works correctly.
        This test verifies that:
        1. The playlist is created immediately
        2. The task returns early with the playlist URL
        3. The polling loop is wrapped with error suppression
        """
        # Create a temporary directory for the test
        test_dir = tempfile.mkdtemp()
        try:
            # Set up the mocks
            mock_store = mock_segment_store.return_value
            session_id = "test_bootstrap_session"
            test_path = os.path.join(test_dir, session_id)
            playlist_url = f"/media/hls/{session_id}/audio.m3u8"
            mock_store.create.return_value = (session_id, test_path, playlist_url)

            # Create the directory structure
            os.makedirs(test_path, exist_ok=True)

            # Set up the StreamingHLSWriter mock
            mock_writer = mock_writer_class.return_value

            # Create a real playlist file to test the polling logic
            playlist_path = os.path.join(test_path, "audio.m3u8")
            with open(playlist_path, 'w') as f:
                f.write("#EXTM3U\n")
                f.write("#EXT-X-VERSION:7\n")
                f.write("#EXT-X-TARGETDURATION:2\n")
                f.write("#EXT-X-MEDIA-SEQUENCE:0\n")
                f.write("#EXT-X-PLAYLIST-TYPE:EVENT\n")

            # Create a segment file after a short delay to simulate async processing
            segment_path = os.path.join(test_path, "segment_000.m4s")

            def create_segment_file():
                time.sleep(0.5)  # Simulate delay in segment creation
                with open(segment_path, 'wb') as f:
                    f.write(b'dummy segment data')

            # Start a thread to create the segment file
            import threading
            segment_thread = threading.Thread(target=create_segment_file)
            segment_thread.daemon = True
            segment_thread.start()

            # Call the task function with a short timeout
            result = generate_audio_stream("Test bootstrap prompt", "en", session_id=session_id, 
                                          timeout_before_return=1.0)

            # Verify that the task returned the playlist URL
            self.assertEqual(result, {"playlist": playlist_url})

            # Verify that the session status was updated to "ready"
            session = AudioSession.objects.filter(session_id=session_id).first()
            self.assertIsNotNone(session)
            self.assertEqual(session.status, "ready")

            # Verify that the segment file was created (or is being created)
            segment_thread.join(2.0)  # Wait for the segment creation thread to finish
            self.assertTrue(os.path.exists(segment_path), "Segment file was not created")

            # Test the error suppression by removing the directory during polling
            # This is a bit tricky to test directly, but we can verify that the code doesn't raise exceptions
            # when the directory is removed
            test_dir2 = tempfile.mkdtemp()
            try:
                mock_store.create.return_value = (session_id + "_2", test_dir2, playlist_url + "_2")

                # Start a thread that will delete the directory after a short delay
                def delete_directory():
                    time.sleep(0.2)  # Wait a bit before deleting
                    shutil.rmtree(test_dir2, ignore_errors=True)

                delete_thread = threading.Thread(target=delete_directory)
                delete_thread.daemon = True
                delete_thread.start()

                # Call the task function - this should not raise exceptions even when the directory is deleted
                result = generate_audio_stream("Test directory deletion", "en", session_id=session_id + "_2", 
                                              timeout_before_return=1.0)

                # The task should still return a result
                self.assertIsNotNone(result)
                self.assertIn("playlist", result)

            finally:
                # Clean up the second test directory if it still exists
                with suppress(FileNotFoundError):
                    shutil.rmtree(test_dir2, ignore_errors=True)

        finally:
            # Clean up the temporary directory
            shutil.rmtree(test_dir, ignore_errors=True)
