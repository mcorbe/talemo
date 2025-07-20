import os
import sys
import logging
import subprocess
import tempfile
from audiostream import tts

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_speak_chunk_to_ffmpeg():
    """Test that the speak_chunk_to_ffmpeg function works correctly."""
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
        tts.speak_chunk_to_ffmpeg(test_text, "en", ffmpeg_process.stdin)

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
