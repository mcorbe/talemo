import io
import unittest
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase
from talemo.audiostream import tts


class TestTTSFunctions(TestCase):
    """Test cases for the TTS module."""

    @patch('talemo.audiostream.tts.gTTS')
    def test_speak_chunk_to_ffmpeg_success(self, mock_gtts_class):
        """Test successful text-to-speech conversion."""
        # Mock gTTS instance
        mock_tts = Mock()
        mock_gtts_class.return_value = mock_tts
        
        # Mock the MP3 data
        test_mp3_data = b'fake mp3 data'
        mock_mp3_buffer = io.BytesIO(test_mp3_data)
        
        def write_to_fp(fp):
            fp.write(test_mp3_data)
        
        mock_tts.write_to_fp.side_effect = write_to_fp
        
        # Mock ffmpeg stdin
        mock_stdin = Mock()
        mock_stdin.closed = False
        
        # Call the function
        tts.speak_chunk_to_ffmpeg("Hello world", "en", mock_stdin)
        
        # Assertions
        mock_gtts_class.assert_called_once_with(text="Hello world", lang="en", slow=False)
        mock_tts.write_to_fp.assert_called_once()
        mock_stdin.write.assert_called_once_with(test_mp3_data)
        mock_stdin.flush.assert_called_once()

    @patch('talemo.audiostream.tts.gTTS')
    def test_speak_chunk_to_ffmpeg_empty_text(self, mock_gtts_class):
        """Test with empty text - should skip TTS."""
        mock_stdin = Mock()
        
        # Call with empty text
        tts.speak_chunk_to_ffmpeg("", "en", mock_stdin)
        
        # Should not call gTTS
        mock_gtts_class.assert_not_called()
        mock_stdin.write.assert_not_called()

    @patch('talemo.audiostream.tts.gTTS')
    def test_speak_chunk_to_ffmpeg_closed_stdin(self, mock_gtts_class):
        """Test with closed stdin - should return early."""
        mock_stdin = Mock()
        mock_stdin.closed = True
        
        # Call the function
        tts.speak_chunk_to_ffmpeg("Hello world", "en", mock_stdin)
        
        # Should not call gTTS
        mock_gtts_class.assert_not_called()
        mock_stdin.write.assert_not_called()

    @patch('talemo.audiostream.tts.gTTS')
    @patch('talemo.audiostream.tts.logger')
    def test_speak_chunk_to_ffmpeg_broken_pipe(self, mock_logger, mock_gtts_class):
        """Test BrokenPipeError handling."""
        # Mock gTTS
        mock_tts = Mock()
        mock_gtts_class.return_value = mock_tts
        test_mp3_data = b'fake mp3 data'
        
        def write_to_fp(fp):
            fp.write(test_mp3_data)
        
        mock_tts.write_to_fp.side_effect = write_to_fp
        
        # Mock stdin that raises BrokenPipeError
        mock_stdin = Mock()
        mock_stdin.closed = False
        mock_stdin.write.side_effect = BrokenPipeError()
        
        # Call should not raise exception
        tts.speak_chunk_to_ffmpeg("Hello world", "en", mock_stdin)
        
        # Should log the error
        mock_logger.error.assert_called_once()

    @patch('talemo.audiostream.tts.gTTS')
    @patch('talemo.audiostream.tts.logger')
    def test_speak_chunk_to_ffmpeg_gtts_error(self, mock_logger, mock_gtts_class):
        """Test gTTS error handling."""
        # Mock gTTS to raise exception
        mock_gtts_class.side_effect = Exception("gTTS error")
        
        mock_stdin = Mock()
        mock_stdin.closed = False
        
        # Call should not raise exception
        tts.speak_chunk_to_ffmpeg("Hello world", "en", mock_stdin)
        
        # Should log the error
        mock_logger.error.assert_called_once()
        self.assertIn("gTTS error", mock_logger.error.call_args[0][0])

    @patch('talemo.audiostream.tts.gTTS')
    def test_speak_chunk_to_ffmpeg_empty_mp3_data(self, mock_gtts_class):
        """Test when gTTS generates empty MP3 data."""
        # Mock gTTS instance
        mock_tts = Mock()
        mock_gtts_class.return_value = mock_tts
        
        # Mock empty MP3 data
        def write_to_fp(fp):
            pass  # Write nothing
        
        mock_tts.write_to_fp.side_effect = write_to_fp
        
        # Mock ffmpeg stdin
        mock_stdin = Mock()
        mock_stdin.closed = False
        
        # Call the function
        tts.speak_chunk_to_ffmpeg("Hello world", "en", mock_stdin)
        
        # Should not write to stdin
        mock_stdin.write.assert_not_called()

    def test_speak_chunk_to_ffmpeg_whitespace_only(self):
        """Test with whitespace-only text."""
        mock_stdin = Mock()
        mock_stdin.closed = False
        
        # Call with whitespace
        tts.speak_chunk_to_ffmpeg("   \n\t  ", "en", mock_stdin)
        
        # Should not write anything
        mock_stdin.write.assert_not_called()

    @patch('talemo.audiostream.tts.gTTS')
    def test_speak_chunk_to_ffmpeg_long_text(self, mock_gtts_class):
        """Test with very long text."""
        # Mock gTTS
        mock_tts = Mock()
        mock_gtts_class.return_value = mock_tts
        test_mp3_data = b'fake mp3 data for long text'
        
        def write_to_fp(fp):
            fp.write(test_mp3_data)
        
        mock_tts.write_to_fp.side_effect = write_to_fp
        
        # Mock stdin
        mock_stdin = Mock()
        mock_stdin.closed = False
        
        # Long text
        long_text = "This is a very long text. " * 100
        
        # Call the function
        tts.speak_chunk_to_ffmpeg(long_text, "en", mock_stdin)
        
        # Should process normally
        mock_gtts_class.assert_called_once_with(text=long_text, lang="en", slow=False)
        mock_stdin.write.assert_called_once_with(test_mp3_data)

    @patch('talemo.audiostream.tts.gTTS')
    def test_speak_chunk_to_ffmpeg_different_languages(self, mock_gtts_class):
        """Test with different language codes."""
        mock_tts = Mock()
        mock_gtts_class.return_value = mock_tts
        test_mp3_data = b'fake mp3 data'
        
        def write_to_fp(fp):
            fp.write(test_mp3_data)
        
        mock_tts.write_to_fp.side_effect = write_to_fp
        
        mock_stdin = Mock()
        mock_stdin.closed = False
        
        # Test different languages
        languages = ['en', 'es', 'fr', 'de', 'it']
        for lang in languages:
            mock_gtts_class.reset_mock()
            mock_stdin.reset_mock()
            
            tts.speak_chunk_to_ffmpeg("Hello", lang, mock_stdin)
            
            mock_gtts_class.assert_called_once_with(text="Hello", lang=lang, slow=False)


class TestTTSIntegration(TestCase):
    """Integration tests for TTS functionality."""

    @patch('subprocess.Popen')
    @patch('talemo.audiostream.tts.gTTS')
    def test_integration_with_ffmpeg_mock(self, mock_gtts_class, mock_popen):
        """Test integration with mocked FFmpeg process."""
        # Mock gTTS
        mock_tts = Mock()
        mock_gtts_class.return_value = mock_tts
        test_mp3_data = b'fake mp3 data'
        
        def write_to_fp(fp):
            fp.write(test_mp3_data)
        
        mock_tts.write_to_fp.side_effect = write_to_fp
        
        # Mock FFmpeg process
        mock_process = Mock()
        mock_stdin = Mock()
        mock_stdin.closed = False
        mock_process.stdin = mock_stdin
        mock_process.poll.return_value = None  # Process is running
        mock_popen.return_value = mock_process
        
        # Simulate the test_speak_chunk_to_ffmpeg function
        from talemo.audiostream.tts import test_speak_chunk_to_ffmpeg
        
        # We can't run the actual test as it creates real files,
        # but we can test the components work together
        tts.speak_chunk_to_ffmpeg("Test integration", "en", mock_stdin)
        
        # Verify the flow
        mock_gtts_class.assert_called_once()
        mock_stdin.write.assert_called_once_with(test_mp3_data)