"""
HLS streaming writer for audio content.

This module provides a StreamingHLSWriter class that:
1. Maintains a single long-lived ffmpeg process
2. Streams audio content directly to ffmpeg
3. Creates an HLS playlist with optimized segment duration for low latency
4. Implements LL-HLS flags for minimal latency
"""
import os
import subprocess
import logging
import uuid
import shutil

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StreamingHLSWriter:
    """
    Class for processing audio chunks incrementally and creating HLS audio.

    This class maintains a single long-lived ffmpeg process and streams
    audio output directly to it for true low-latency streaming.
    """

    def __init__(self, output_dir, segment_duration=2):
        """
        Initialize the StreamingHLSWriter instance.

        Args:
            output_dir (str): Path to output directory
            segment_duration (int): Duration of each segment in seconds (default: 2)
        """
        self.segment_duration = segment_duration

        # Create HLS directory
        self.hls_dir = output_dir
        os.makedirs(self.hls_dir, exist_ok=True)

        # Initialize state
        self.chunk_count = 0
        self.ffmpeg_process = None
        self.ffmpeg_stdin = None

        # Start the ffmpeg process
        self._start_ffmpeg_process()

    def _start_ffmpeg_process(self):
        """
        Start a single long-lived ffmpeg process for HLS streaming.
        """
        logger.info("Starting ffmpeg process for HLS streaming")

        # FFmpeg will create the playlist with the temp_file flag
        playlist_path = os.path.join(self.hls_dir, "audio.m3u8")
        logger.info(f"FFmpeg will create/update playlist at {playlist_path}")

        ffmpeg_cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "info",
            "-f", "mp3", "-i", "pipe:0",
            "-c:a", "aac", "-b:a", "128k",
            "-f", "hls",
            # Shorter segments for lower latency
            "-hls_time", "1",
            "-hls_list_size", "10",
            # The *temp_file* flag forces ffmpeg to write to a temporary
            # playlist, then atomically rename it – this guarantees that
            # the file is **always present on disk** and never half-written.
            # We also remove *delete_segments* so that old segments stay
            # available for a short period; this is important for players
            # that start late.
            "-hls_flags", 
              "append_list+independent_segments+program_date_time+temp_file",
            "-hls_segment_type", "fmp4",
            "-hls_init_time", "0.5",
            "-hls_allow_cache", "1",
            "-hls_playlist_type", "event",
            "-hls_segment_filename", os.path.join(self.hls_dir, "segment_%03d.m4s"),
            playlist_path,  # Use the playlist we just created
        ]

        # Ensure the output directory exists
        os.makedirs(self.hls_dir, exist_ok=True)

        # Check if the directory is writable
        if not os.access(self.hls_dir, os.W_OK):
            logger.error(f"Output directory {self.hls_dir} is not writable")
            raise RuntimeError(f"Output directory {self.hls_dir} is not writable")

        # Start the ffmpeg process and capture stderr
        logger.info(f"Running ffmpeg command: {' '.join(ffmpeg_cmd)}")
        self.ffmpeg_process = subprocess.Popen(
            ffmpeg_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.ffmpeg_stdin = self.ffmpeg_process.stdin

        # Check if process started successfully
        import time
        time.sleep(0.1)
        if self.ffmpeg_process.poll() is not None:
            stderr = self.ffmpeg_process.stderr.read().decode()
            logger.error(f"ffmpeg process failed to start: {stderr}")
            raise RuntimeError(f"ffmpeg process failed: {stderr}")

        # Log the FFmpeg PID so it can be killed from the outside if needed
        logger.info(f"FFmpeg process started with PID: {self.ffmpeg_process.pid}")

    def process_chunk(self, audio_data):
        """
        Process a single audio chunk.

        This method streams the audio data directly to the ffmpeg process.

        Args:
            audio_data (bytes): Audio data to process

        Returns:
            dict: Information about the processed chunk
        """
        if not audio_data:
            logger.warning("Empty audio data received, skipping")
            return None

        logger.info(f"Processing audio chunk {self.chunk_count + 1}")

        # Generate a unique ID for this chunk
        chunk_id = f"chunk_{self.chunk_count:03d}_{uuid.uuid4().hex[:8]}"

        # Check if ffmpeg process is still running
        if self.ffmpeg_process is None or self.ffmpeg_process.poll() is not None:
            logger.warning("ffmpeg process is not running, restarting it")

            # The playlist should be created by FFmpeg with the temp_file flag,
            # but check if it exists and log a warning if it doesn't
            playlist_path = os.path.join(self.hls_dir, "audio.m3u8")
            if not os.path.exists(playlist_path) and self.chunk_count > 0:
                logger.warning(f"Playlist file not found at {playlist_path} before restart, which is unexpected")

            self._start_ffmpeg_process()

            # Verify that the process started successfully
            if self.ffmpeg_process is None or self.ffmpeg_process.poll() is not None:
                logger.error("Failed to restart ffmpeg process")
                # Log a warning if the playlist file is missing
                if not os.path.exists(playlist_path):
                    logger.warning(f"Playlist file not found at {playlist_path} after restart attempt, which is unexpected")
                return None

        # Check if stdin is still open
        if self.ffmpeg_stdin is None or self.ffmpeg_stdin.closed:
            logger.warning("ffmpeg stdin is closed, cannot write audio data")
            return None

        # Ensure audio data is valid
        if not isinstance(audio_data, bytes):
            logger.warning(f"Invalid audio data type: {type(audio_data)}, expected bytes")
            return None

        try:
            # Stream audio data directly to ffmpeg
            self.ffmpeg_stdin.write(audio_data)
            self.ffmpeg_stdin.flush()
        except BrokenPipeError:
            logger.error("BrokenPipeError: ffmpeg process may have terminated unexpectedly")
            # Try to restart the ffmpeg process
            self._start_ffmpeg_process()

            # Check if the playlist file exists after restart
            playlist_path = os.path.join(self.hls_dir, "audio.m3u8")
            if not os.path.exists(playlist_path) and self.chunk_count > 0:
                logger.warning(f"Playlist file not found at {playlist_path} after BrokenPipeError, which is unexpected")

            return None
        except Exception as e:
            logger.error(f"Error writing to ffmpeg: {str(e)}")
            return None

        # Update state
        self.chunk_count += 1

        return {
            'chunk_id': chunk_id,
            'hls_dir': self.hls_dir
        }

    def finalize(self):
        """
        Finalize the HLS playlist and close the ffmpeg process.

        Returns:
            dict: Information about the generated HLS stream
        """
        logger.info("Finalizing HLS playlist")

        if self.ffmpeg_process:
            # Close stdin to the signal end of input
            if self.ffmpeg_stdin:
                self.ffmpeg_stdin.close()
                self.ffmpeg_stdin = None

            # Wait for ffmpeg to finish
            logger.info("Waiting for ffmpeg process to finish")
            self.ffmpeg_process.wait()
            self.ffmpeg_process = None

        # The playlist file should already exist since FFmpeg creates it immediately
        # with the temp_file flag, but we'll log if it's missing for debugging
        playlist_path = os.path.join(self.hls_dir, "audio.m3u8")
        if not os.path.exists(playlist_path):
            logger.warning(f"Playlist file not found at {playlist_path} after finalization, which is unexpected")

        # Check for segment files and log them
        segment_files = [f for f in os.listdir(self.hls_dir) if f.endswith('.m4s') or f.startswith('segment_')]
        if segment_files:
            logger.info(f"Found {len(segment_files)} segment files: {', '.join(segment_files)}")
        else:
            logger.warning(f"No segment files found in {self.hls_dir}")
            # List all files in the directory for debugging
            all_files = os.listdir(self.hls_dir)
            logger.info(f"Files in directory: {', '.join(all_files) if all_files else 'none'}")

        return {
            'playlist_path': playlist_path,
            'hls_dir': self.hls_dir,
            'segment_count': len(segment_files),
            'chunk_count': self.chunk_count
        }

    def _create_minimal_playlist(self, playlist_path):
        """
        Create a minimal valid HLS playlist file.

        This creates an empty but syntactically valid playlist that can be served immediately.
        The client will keep polling until new lines appear as segments are generated.

        Args:
            playlist_path (str): Path to the playlist file to create
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(playlist_path), exist_ok=True)

            # Create a minimal valid HLS playlist with just the header lines
            with open(playlist_path, 'w') as f:
                f.write("#EXTM3U\n")
                f.write("#EXT-X-VERSION:7\n")
                f.write("#EXT-X-TARGETDURATION:1\n")
                f.write("#EXT-X-MEDIA-SEQUENCE:0\n")
                f.write("#EXT-X-PLAYLIST-TYPE:EVENT\n")

                # Note: We intentionally don't add any segments or #EXT-X-ENDLIST
                # This allows ffmpeg to append segments as they're generated

            logger.info(f"Created minimal valid HLS playlist at {playlist_path}")

        except Exception as e:
            logger.error(f"Error creating minimal playlist: {str(e)}")

            # Last resort: try to create the playlist in a different location
            try:
                import tempfile
                temp_dir = tempfile.gettempdir()
                alt_playlist_path = os.path.join(temp_dir, "audio.m3u8")

                with open(alt_playlist_path, 'w') as f:
                    f.write("#EXTM3U\n")
                    f.write("#EXT-X-VERSION:7\n")
                    f.write("#EXT-X-TARGETDURATION:1\n")
                    f.write("#EXT-X-MEDIA-SEQUENCE:0\n")
                    f.write("#EXT-X-PLAYLIST-TYPE:EVENT\n")

                logger.warning(f"Created minimal playlist in alternative location: {alt_playlist_path}")

                # Try to copy it to the original location
                try:
                    import shutil
                    shutil.copy2(alt_playlist_path, playlist_path)
                    logger.info(f"Copied playlist from {alt_playlist_path} to {playlist_path}")
                except Exception as copy_e:
                    logger.error(f"Error copying playlist: {str(copy_e)}")
            except Exception as alt_e:
                logger.error(f"Error creating alternative playlist: {str(alt_e)}")

    def __del__(self):
        """Clean up the ffmpeg process if still running."""
        # Close the ffmpeg process if still running
        if self.ffmpeg_process and self.ffmpeg_process.poll() is None:
            if self.ffmpeg_stdin:
                self.ffmpeg_stdin.close()
            self.ffmpeg_process.terminate()
            try:
                self.ffmpeg_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.ffmpeg_process.kill()
