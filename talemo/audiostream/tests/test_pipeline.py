import os
import asyncio
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock, AsyncMock, mock_open
from django.test import TestCase
from talemo.audiostream.pipeline import run_audio_session


class TestPipeline(TestCase):
    """Test cases for the audio pipeline module."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.playlist_path = os.path.join(self.temp_dir, 'audio.m3u8')
        
    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.tts.speak_chunk_to_ffmpeg')
    def test_run_audio_session_basic(self, mock_speak, mock_stream_tokens, mock_writer_class):
        """Test basic audio session with simple text."""
        # Mock the writer
        mock_writer = Mock()
        mock_writer.ffmpeg_process = Mock()
        mock_writer.ffmpeg_process.poll.return_value = None
        mock_writer.ffmpeg_stdin = Mock()
        mock_writer.ffmpeg_stdin.closed = False
        mock_writer.finalize.return_value = {'chunks': 1, 'segment_count': 1}
        mock_writer_class.return_value = mock_writer
        
        # Mock LLM tokens
        async def mock_token_generator():
            tokens = ["Hello", " ", "world", "."]
            for token in tokens:
                yield token
        
        mock_stream_tokens.return_value = mock_token_generator()
        
        # Mock progress callback
        mock_progress = Mock()
        
        # Run the session
        result = run_audio_session(
            prompt="Hello world",
            playlist_path=self.playlist_path,
            lang="en",
            chunk_words=2,
            progress_cb=mock_progress
        )
        
        # Verify writer was created with correct directory
        mock_writer_class.assert_called_once_with(self.temp_dir)
        
        # Verify TTS was called
        mock_speak.assert_called()
        
        # Verify progress callbacks
        mock_progress.assert_any_call("chunk", {"chunk_count": 1})
        mock_progress.assert_any_call("done", {'chunks': 1, 'segment_count': 1})

    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.tts.speak_chunk_to_ffmpeg')
    @patch('builtins.open', new_callable=mock_open)
    def test_run_audio_session_with_logging(self, mock_file, mock_speak, mock_stream_tokens, mock_writer_class):
        """Test that text chunks are logged to file."""
        # Mock the writer
        mock_writer = Mock()
        mock_writer.ffmpeg_process = Mock()
        mock_writer.ffmpeg_process.poll.return_value = None
        mock_writer.ffmpeg_stdin = Mock()
        mock_writer.ffmpeg_stdin.closed = False
        mock_writer.finalize.return_value = {'chunks': 1, 'segment_count': 1}
        mock_writer_class.return_value = mock_writer
        
        # Mock LLM tokens
        async def mock_token_generator():
            tokens = ["This", " ", "is", " ", "a", " ", "test", "."]
            for token in tokens:
                yield token
        
        mock_stream_tokens.return_value = mock_token_generator()
        
        # Run the session
        run_audio_session(
            prompt="Test prompt",
            playlist_path=self.playlist_path,
            lang="en",
            chunk_words=10
        )
        
        # Verify log file was created and written to
        expected_log_path = os.path.join(self.temp_dir, 'text_chunks.log')
        mock_file.assert_any_call(expected_log_path, 'w', encoding='utf-8')
        mock_file.assert_any_call(expected_log_path, 'a', encoding='utf-8')
        
        # Check initial header was written
        handle = mock_file()
        handle.write.assert_any_call("=== Audio Generation Session ===\n")
        handle.write.assert_any_call("Original prompt: Test prompt\n")

    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.tts.speak_chunk_to_ffmpeg')
    def test_run_audio_session_multiple_chunks(self, mock_speak, mock_stream_tokens, mock_writer_class):
        """Test processing multiple text chunks."""
        # Mock the writer
        mock_writer = Mock()
        mock_writer.ffmpeg_process = Mock()
        mock_writer.ffmpeg_process.poll.return_value = None
        mock_writer.ffmpeg_stdin = Mock()
        mock_writer.ffmpeg_stdin.closed = False
        mock_writer.finalize.return_value = {'chunks': 3, 'segment_count': 3}
        mock_writer_class.return_value = mock_writer
        
        # Mock LLM tokens that will create multiple chunks
        async def mock_token_generator():
            # First chunk (punctuation-based)
            tokens1 = ["First", " ", "sentence", "."]
            for token in tokens1:
                yield token
            
            # Second chunk (punctuation-based)
            tokens2 = [" ", "Second", " ", "one", "!"]
            for token in tokens2:
                yield token
                
            # Third chunk (punctuation-based)
            tokens3 = [" ", "Third", "?"]
            for token in tokens3:
                yield token
        
        mock_stream_tokens.return_value = mock_token_generator()
        
        # Run the session
        result = run_audio_session(
            prompt="Multiple sentences",
            playlist_path=self.playlist_path,
            chunk_words=40  # High limit to test punctuation-based chunking
        )
        
        # Should have called TTS for each chunk
        self.assertEqual(mock_speak.call_count, 3)
        
        # Verify the text chunks
        calls = mock_speak.call_args_list
        self.assertEqual(calls[0][0][0], "First sentence.")
        self.assertEqual(calls[1][0][0], " Second one!")
        self.assertEqual(calls[2][0][0], " Third?")

    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.tts.speak_chunk_to_ffmpeg')
    def test_run_audio_session_ffmpeg_restart(self, mock_speak, mock_stream_tokens, mock_writer_class):
        """Test that FFmpeg process is restarted when it dies."""
        # Mock the writer
        mock_writer = Mock()
        mock_writer.ffmpeg_process = Mock()
        mock_writer.ffmpeg_stdin = Mock()
        mock_writer.finalize.return_value = {'chunks': 1, 'segment_count': 1}
        mock_writer_class.return_value = mock_writer
        
        # Simulate FFmpeg process dying
        mock_writer.ffmpeg_process.poll.side_effect = [1, None, None]  # Dead, then alive
        mock_writer.ffmpeg_stdin.closed = False
        
        # Mock LLM tokens
        async def mock_token_generator():
            yield "Hello."
        
        mock_stream_tokens.return_value = mock_token_generator()
        
        # Run the session
        run_audio_session(
            prompt="Test",
            playlist_path=self.playlist_path
        )
        
        # Should have restarted FFmpeg
        mock_writer._start_ffmpeg_process.assert_called()

    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.tts.speak_chunk_to_ffmpeg')
    @patch('talemo.audiostream.pipeline.logger')
    def test_run_audio_session_tts_error_handling(self, mock_logger, mock_speak, mock_stream_tokens, mock_writer_class):
        """Test error handling when TTS fails."""
        # Mock the writer
        mock_writer = Mock()
        mock_writer.ffmpeg_process = Mock()
        mock_writer.ffmpeg_process.poll.return_value = None
        mock_writer.ffmpeg_stdin = Mock()
        mock_writer.ffmpeg_stdin.closed = False
        mock_writer.finalize.return_value = {'chunks': 0, 'segment_count': 0}
        mock_writer_class.return_value = mock_writer
        
        # Mock TTS to raise exception
        mock_speak.side_effect = Exception("TTS error")
        
        # Mock LLM tokens
        async def mock_token_generator():
            yield "Hello."
        
        mock_stream_tokens.return_value = mock_token_generator()
        
        # Run the session - should not raise
        result = run_audio_session(
            prompt="Test",
            playlist_path=self.playlist_path
        )
        
        # Should have logged the error
        mock_logger.error.assert_any_call("Error in speak_chunk_to_ffmpeg: TTS error")

    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.tts.speak_chunk_to_ffmpeg')
    def test_run_audio_session_first_chunk_optimization(self, mock_speak, mock_stream_tokens, mock_writer_class):
        """Test that first chunk is sent early for faster startup."""
        # Mock the writer
        mock_writer = Mock()
        mock_writer.ffmpeg_process = Mock()
        mock_writer.ffmpeg_process.poll.return_value = None
        mock_writer.ffmpeg_stdin = Mock()
        mock_writer.ffmpeg_stdin.closed = False
        mock_writer.finalize.return_value = {'chunks': 2, 'segment_count': 2}
        mock_writer_class.return_value = mock_writer
        
        # Mock LLM tokens - first chunk should be sent after 10 words
        async def mock_token_generator():
            # Generate exactly 10 words for first chunk
            for i in range(10):
                yield f"word{i} "
            # Then more words
            for i in range(10, 20):
                yield f"word{i} "
            yield "."
        
        mock_stream_tokens.return_value = mock_token_generator()
        
        # Run the session
        run_audio_session(
            prompt="Test",
            playlist_path=self.playlist_path,
            chunk_words=40  # High limit
        )
        
        # Should have two chunks
        self.assertEqual(mock_speak.call_count, 2)
        
        # First chunk should have exactly 10 words
        first_chunk = mock_speak.call_args_list[0][0][0]
        word_count = len(first_chunk.strip().split())
        self.assertEqual(word_count, 10)

    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.logger')
    def test_run_audio_session_llm_error(self, mock_logger, mock_stream_tokens, mock_writer_class):
        """Test error handling when LLM fails."""
        # Mock the writer
        mock_writer = Mock()
        mock_writer.finalize.return_value = {'chunks': 0, 'segment_count': 0}
        mock_writer_class.return_value = mock_writer
        
        # Mock LLM to raise exception
        async def mock_token_generator():
            raise Exception("LLM error")
            yield  # Make it a generator
        
        mock_stream_tokens.return_value = mock_token_generator()
        
        # Run the session
        result = run_audio_session(
            prompt="Test",
            playlist_path=self.playlist_path
        )
        
        # Should have logged the error
        mock_logger.error.assert_any_call("Error in stream_tokens: LLM error")

    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.tts.speak_chunk_to_ffmpeg')
    @patch('os.path.exists')
    @patch('talemo.audiostream.pipeline.logger')
    def test_run_audio_session_missing_playlist_warning(self, mock_logger, mock_exists, mock_speak, mock_stream_tokens, mock_writer_class):
        """Test warning when playlist file is not created."""
        # Mock the writer
        mock_writer = Mock()
        mock_writer.ffmpeg_process = Mock()
        mock_writer.ffmpeg_process.poll.return_value = None
        mock_writer.ffmpeg_stdin = Mock()
        mock_writer.ffmpeg_stdin.closed = False
        mock_writer.finalize.return_value = {'chunks': 1, 'segment_count': 1}
        mock_writer_class.return_value = mock_writer
        
        # Mock playlist doesn't exist
        mock_exists.return_value = False
        
        # Mock LLM tokens
        async def mock_token_generator():
            yield "Hello."
        
        mock_stream_tokens.return_value = mock_token_generator()
        
        # Run the session
        run_audio_session(
            prompt="Test",
            playlist_path=self.playlist_path
        )
        
        # Should have logged warning
        mock_logger.warning.assert_any_call(
            f"Playlist file still not created after finalize: {self.playlist_path}, which is unexpected with FFmpeg temp_file flag"
        )

    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.tts.speak_chunk_to_ffmpeg')
    def test_run_audio_session_word_based_chunking(self, mock_speak, mock_stream_tokens, mock_writer_class):
        """Test word-based chunking when no punctuation."""
        # Mock the writer
        mock_writer = Mock()
        mock_writer.ffmpeg_process = Mock()
        mock_writer.ffmpeg_process.poll.return_value = None
        mock_writer.ffmpeg_stdin = Mock()
        mock_writer.ffmpeg_stdin.closed = False
        mock_writer.finalize.return_value = {'chunks': 2, 'segment_count': 2}
        mock_writer_class.return_value = mock_writer
        
        # Mock LLM tokens without punctuation
        async def mock_token_generator():
            # Generate tokens that will exceed chunk_words limit
            for i in range(15):
                yield f"word{i} "
        
        mock_stream_tokens.return_value = mock_token_generator()
        
        # Run with small chunk size
        run_audio_session(
            prompt="Test",
            playlist_path=self.playlist_path,
            chunk_words=10
        )
        
        # Should have created multiple chunks
        self.assertGreaterEqual(mock_speak.call_count, 1)

    @patch('talemo.audiostream.pipeline.StreamingHLSWriter')
    @patch('talemo.audiostream.pipeline.llm.stream_tokens')
    @patch('talemo.audiostream.pipeline.tts.speak_chunk_to_ffmpeg')
    @patch('talemo.audiostream.pipeline.logger')
    def test_run_audio_session_finalize_error(self, mock_logger, mock_speak, mock_stream_tokens, mock_writer_class):
        """Test error handling during finalization."""
        # Mock the writer
        mock_writer = Mock()
        mock_writer.ffmpeg_process = Mock()
        mock_writer.ffmpeg_process.poll.return_value = None
        mock_writer.ffmpeg_stdin = Mock()
        mock_writer.ffmpeg_stdin.closed = False
        mock_writer.finalize.side_effect = Exception("Finalize error")
        mock_writer_class.return_value = mock_writer
        
        # Mock LLM tokens
        async def mock_token_generator():
            yield "Hello."
        
        mock_stream_tokens.return_value = mock_token_generator()
        
        # Run the session
        result = run_audio_session(
            prompt="Test",
            playlist_path=self.playlist_path
        )
        
        # Should have logged the error
        mock_logger.error.assert_any_call("Error finalizing HLS playlist: Finalize error")
        
        # Should still return None (no result)
        self.assertIsNone(result)