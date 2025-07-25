from gtts import gTTS
import logging
import io
import time
import os
import sys
import subprocess
import tempfile

logger = logging.getLogger(__name__)

def speak_chunk_to_ffmpeg(text: str, lang: str, ffmpeg_stdin):
    if not text.strip():
        logger.warning("Empty text received, skipping TTS")
        return

    if ffmpeg_stdin.closed:
        logger.error("Cannot write to ffmpeg: stdin is closed")
        return

    try:
        logger.info(f"Converting text to speech: '{text[:50]}{'...' if len(text) > 50 else ''}'")

        # Create a gTTS object
        tts = gTTS(text=text, lang=lang, slow=False)

        # First, try to get the full MP3 data to validate it
        mp3_data = io.BytesIO()
        tts.write_to_fp(mp3_data)
        mp3_data.seek(0)
        data = mp3_data.read()

        if not data:
            logger.error("gTTS generated empty MP3 data")
            return

        logger.info(f"Generated {len(data)} bytes of MP3 data")

        # Write the data to ffmpeg's stdin
        ffmpeg_stdin.write(data)
        ffmpeg_stdin.flush()

        # Small delay to allow ffmpeg to process the data
        time.sleep(0.1)

        logger.info("Successfully wrote MP3 data to ffmpeg")
    except BrokenPipeError:
        logger.error("BrokenPipeError: ffmpeg process may have terminated unexpectedly")
        # Don't re-raise the exception, just log it and continue
    except Exception as e:
        logger.error(f"Error in speak_chunk_to_ffmpeg: {str(e)}")
        # Don't re-raise other exceptions either, just log them

def test_speak_chunk_to_ffmpeg():
    """Test that the speak_chunk_to_ffmpeg function works correctly."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Create a temporary directory for the output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up ffmpeg command to create an MP3 file
        output_file = os.path.join(temp_dir, "output.mp3")
        ffmpeg_cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "info",
            "-f", "mp3", "-i", "pipe:0",
            "-c:a", "copy",
            output_file
        ]

        # Start ffmpeg process
        logger.info(f"Starting ffmpeg process: {' '.join(ffmpeg_cmd)}")
        ffmpeg_process = subprocess.Popen(
            ffmpeg_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Test text
        test_text = "This is a test of the text-to-speech functionality."

        # Call the speak_chunk_to_ffmpeg function
        logger.info(f"Converting text to speech: '{test_text}'")
        speak_chunk_to_ffmpeg(test_text, "en", ffmpeg_process.stdin)

        # Close stdin to signal end of input
        ffmpeg_process.stdin.close()

        # Wait for ffmpeg to finish
        ffmpeg_process.wait()

        # Check if the output file was created and has content
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            logger.info(f"Success! Created MP3 file with size {os.path.getsize(output_file)} bytes")
            return True
        else:
            logger.error("Failed to create MP3 file")
            stderr = ffmpeg_process.stderr.read().decode()
            logger.error(f"ffmpeg stderr: {stderr}")
            return False

if __name__ == "__main__":
    success = test_speak_chunk_to_ffmpeg()
    sys.exit(0 if success else 1)
