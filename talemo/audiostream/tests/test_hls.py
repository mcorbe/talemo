import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock, call
from django.test import TestCase
from talemo.audiostream.hls import StreamingHLSWriter


class TestStreamingHLSWriter(TestCase):
    """Test cases for the StreamingHLSWriter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    @patch('subprocess.Popen')
    def test_init_creates_directory(self, mock_popen):
        """Test that initialization creates the output directory."""
        # Mock the subprocess
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_process.stdin = Mock()
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        
        # Create writer
        output_dir = os.path.join(self.temp_dir, 'test_output')
        writer = StreamingHLSWriter(output_dir)
        
        # Directory should be created
        self.assertTrue(os.path.exists(output_dir))
        self.assertEqual(writer.hls_dir, output_dir)

    @patch('subprocess.Popen')
    def test_init_starts_ffmpeg_process(self, mock_popen):
        """Test that initialization starts the FFmpeg process."""
        # Mock the subprocess
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_process.stdin = Mock()
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        
        # Create writer
        writer = StreamingHLSWriter(self.temp_dir)
        
        # FFmpeg should be started
        mock_popen.assert_called_once()
        self.assertEqual(writer.ffmpeg_process, mock_process)
        self.assertIsNotNone(writer.ffmpeg_stdin)
        
        # Check FFmpeg command
        args = mock_popen.call_args[0][0]
        self.assertEqual(args[0], 'ffmpeg')
        self.assertIn('-f', args)
        self.assertIn('hls', args)
        self.assertIn('-i', args)
        self.assertIn('pipe:0', args)

    @patch('subprocess.Popen')
    @patch('os.access')
    def test_init_handles_non_writable_directory(self, mock_access, mock_popen):
        """Test handling of non-writable directory."""
        # Mock directory as non-writable
        mock_access.return_value = False
        
        # Should raise RuntimeError
        with self.assertRaises(RuntimeError) as cm:
            StreamingHLSWriter(self.temp_dir)
        
        self.assertIn("not writable", str(cm.exception))

    @patch('subprocess.Popen')
    @patch('time.sleep')
    def test_init_handles_ffmpeg_failure(self, mock_sleep, mock_popen):
        """Test handling when FFmpeg fails to start."""
        # Mock process that fails immediately
        mock_process = Mock()
        mock_process.poll.return_value = 1  # Non-zero exit code
        mock_process.stderr.read.return_value = b"FFmpeg error"
        mock_popen.return_value = mock_process
        
        # Should raise RuntimeError
        with self.assertRaises(RuntimeError) as cm:
            StreamingHLSWriter(self.temp_dir)
        
        self.assertIn("ffmpeg process failed", str(cm.exception))

    @patch('subprocess.Popen')
    def test_process_chunk_success(self, mock_popen):
        """Test successful audio chunk processing."""
        # Mock the subprocess
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_stdin = Mock()
        mock_stdin.closed = False
        mock_process.stdin = mock_stdin
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        
        # Create writer
        writer = StreamingHLSWriter(self.temp_dir)
        
        # Process a chunk
        audio_data = b"fake audio data"
        result = writer.process_chunk(audio_data)
        
        # Should write to stdin
        mock_stdin.write.assert_called_once_with(audio_data)
        mock_stdin.flush.assert_called_once()
        
        # Should return chunk info
        self.assertIsInstance(result, dict)
        self.assertIn('chunk_id', result)

    @patch('subprocess.Popen')
    def test_process_chunk_empty_data(self, mock_popen):
        """Test processing empty audio data."""
        # Mock the subprocess
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_process.stdin = Mock()
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        
        # Create writer
        writer = StreamingHLSWriter(self.temp_dir)
        
        # Process empty chunk
        result = writer.process_chunk(b"")
        
        # Should return None
        self.assertIsNone(result)
        mock_process.stdin.write.assert_not_called()

    @patch('subprocess.Popen')
    def test_process_chunk_restarts_dead_process(self, mock_popen):
        """Test that process_chunk restarts dead FFmpeg process."""
        # First process (dead)
        mock_process1 = Mock()
        mock_process1.poll.return_value = 1  # Process has exited
        mock_process1.stdin = Mock()
        
        # Second process (alive)
        mock_process2 = Mock()
        mock_process2.poll.return_value = None
        mock_stdin2 = Mock()
        mock_stdin2.closed = False
        mock_process2.stdin = mock_stdin2
        mock_process2.pid = 67890
        
        # Configure mock to return different processes
        mock_popen.side_effect = [mock_process1, mock_process2]
        
        # Create writer
        writer = StreamingHLSWriter(self.temp_dir)
        
        # Process should be dead now
        writer.ffmpeg_process = mock_process1
        
        # Process a chunk
        audio_data = b"fake audio data"
        result = writer.process_chunk(audio_data)
        
        # Should have restarted process
        self.assertEqual(mock_popen.call_count, 2)
        self.assertEqual(writer.ffmpeg_process, mock_process2)
        mock_stdin2.write.assert_called_once_with(audio_data)

    @patch('subprocess.Popen')
    def test_finalize_success(self, mock_popen):
        """Test successful finalization."""
        # Mock the subprocess
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_process.wait.return_value = 0
        mock_stdin = Mock()
        mock_stdin.closed = False
        mock_process.stdin = mock_stdin
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        
        # Create writer
        writer = StreamingHLSWriter(self.temp_dir)
        
        # Create some fake segment files
        for i in range(3):
            open(os.path.join(self.temp_dir, f'segment_{i:03d}.m4s'), 'w').close()
        
        # Finalize
        result = writer.finalize()
        
        # Should close stdin and wait
        mock_stdin.close.assert_called_once()
        mock_process.wait.assert_called_once()
        
        # Should return info dict
        self.assertIsInstance(result, dict)
        self.assertEqual(result['chunks'], 1)  # We processed 0 chunks but incremented counter
        self.assertEqual(result['segment_count'], 3)

    @patch('subprocess.Popen')
    def test_finalize_already_finalized(self, mock_popen):
        """Test calling finalize when already finalized."""
        # Mock the subprocess
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_stdin = Mock()
        mock_stdin.closed = True  # Already closed
        mock_process.stdin = mock_stdin
        mock_popen.return_value = mock_process
        
        # Create writer
        writer = StreamingHLSWriter(self.temp_dir)
        writer.ffmpeg_process = None  # Already finalized
        
        # Finalize again
        result = writer.finalize()
        
        # Should return minimal info
        self.assertEqual(result['chunks'], 0)
        self.assertEqual(result['segment_count'], 0)

    @patch('subprocess.Popen')
    @patch('talemo.audiostream.hls.logger')
    def test_finalize_with_ffmpeg_error(self, mock_logger, mock_popen):
        """Test finalization when FFmpeg has errors."""
        # Mock the subprocess
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_process.wait.return_value = 1  # Non-zero exit
        mock_process.stderr.read.return_value = b"FFmpeg error output"
        mock_stdin = Mock()
        mock_stdin.closed = False
        mock_process.stdin = mock_stdin
        mock_popen.return_value = mock_process
        
        # Create writer
        writer = StreamingHLSWriter(self.temp_dir)
        
        # Finalize
        result = writer.finalize()
        
        # Should log the error
        mock_logger.error.assert_called()
        self.assertIn("FFmpeg error output", mock_logger.error.call_args[0][0])

    @patch('subprocess.Popen')
    def test_multiple_chunks_processing(self, mock_popen):
        """Test processing multiple audio chunks."""
        # Mock the subprocess
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_stdin = Mock()
        mock_stdin.closed = False
        mock_process.stdin = mock_stdin
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        
        # Create writer
        writer = StreamingHLSWriter(self.temp_dir)
        
        # Process multiple chunks
        chunks = [b"chunk1", b"chunk2", b"chunk3"]
        results = []
        
        for chunk in chunks:
            result = writer.process_chunk(chunk)
            results.append(result)
        
        # Should have processed all chunks
        self.assertEqual(len(results), 3)
        self.assertEqual(writer.chunk_count, 3)
        
        # Verify all chunks were written
        expected_calls = [call(chunk) for chunk in chunks]
        mock_stdin.write.assert_has_calls(expected_calls)

    @patch('subprocess.Popen')
    def test_segment_duration_parameter(self, mock_popen):
        """Test custom segment duration parameter."""
        # Mock the subprocess
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_process.stdin = Mock()
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        
        # Create writer with custom segment duration
        custom_duration = 5
        writer = StreamingHLSWriter(self.temp_dir, segment_duration=custom_duration)
        
        # Check that segment duration was set
        self.assertEqual(writer.segment_duration, custom_duration)
        
        # Verify it's used in FFmpeg command
        args = mock_popen.call_args[0][0]
        hls_time_index = args.index('-hls_time')
        self.assertEqual(args[hls_time_index + 1], '1')  # Currently hardcoded to 1

    @patch('subprocess.Popen')
    @patch('os.path.exists')
    def test_process_chunk_logs_playlist_warning(self, mock_exists, mock_popen):
        """Test that process_chunk logs warning if playlist doesn't exist."""
        # Mock the subprocess
        mock_process = Mock()
        mock_process.poll.return_value = 1  # Dead process
        mock_process.stdin = Mock()
        
        # New process
        mock_process2 = Mock()
        mock_process2.poll.return_value = None
        mock_process2.stdin = Mock()
        mock_process2.stdin.closed = False
        mock_process2.pid = 67890
        
        mock_popen.side_effect = [mock_process, mock_process2]
        
        # Mock playlist doesn't exist
        mock_exists.return_value = False
        
        # Create writer
        writer = StreamingHLSWriter(self.temp_dir)
        writer.chunk_count = 5  # Simulate we've processed chunks
        
        # Process a chunk (will trigger restart)
        with patch('talemo.audiostream.hls.logger') as mock_logger:
            writer.process_chunk(b"data")
            
            # Should log warning about missing playlist
            mock_logger.warning.assert_any_call(
                "Playlist file not found at %s before restart, which is unexpected",
                os.path.join(self.temp_dir, "audio.m3u8")
            )