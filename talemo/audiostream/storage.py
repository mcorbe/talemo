import os, uuid, shutil
from django.conf import settings
import tempfile
import logging
import platform

logger = logging.getLogger(__name__)

class SegmentStore:
    def __init__(self):
        # Store the expected directory for HLS files
        self.expected_dir = None
        if hasattr(settings, 'HLS_ROOT') and os.path.isabs(settings.HLS_ROOT):
            self.expected_dir = settings.HLS_ROOT
        elif hasattr(settings, 'MEDIA_ROOT'):
            self.expected_dir = os.path.join(settings.MEDIA_ROOT, 'hls')

        # Use a directory that is guaranteed to be writable
        # First try the configured HLS_ROOT
        if hasattr(settings, 'HLS_ROOT') and os.path.isabs(settings.HLS_ROOT):
            try:
                os.makedirs(settings.HLS_ROOT, exist_ok=True)
                if os.access(settings.HLS_ROOT, os.W_OK):
                    self.base_dir = settings.HLS_ROOT
                    logger.info(f"Using configured HLS_ROOT directory: {self.base_dir}")
                else:
                    logger.warning(f"HLS_ROOT directory is not writable: {settings.HLS_ROOT}")
            except Exception as e:
                logger.warning(f"Error creating HLS_ROOT directory: {str(e)}")

        # If we don't have a base_dir yet, try the media/hls directory
        if not hasattr(self, 'base_dir'):
            try:
                media_hls_dir = os.path.join(settings.MEDIA_ROOT, 'hls')
                os.makedirs(media_hls_dir, exist_ok=True)
                if os.access(media_hls_dir, os.W_OK):
                    self.base_dir = media_hls_dir
                    logger.info(f"Using media/hls directory: {self.base_dir}")
                else:
                    logger.warning(f"media/hls directory is not writable: {media_hls_dir}")
            except Exception as e:
                logger.warning(f"Error creating media/hls directory: {str(e)}")

        # If we still don't have a base_dir, try /app/media/hls directory (Docker container path)
        if not hasattr(self, 'base_dir'):
            try:
                docker_hls_dir = "/app/media/hls"
                os.makedirs(docker_hls_dir, exist_ok=True)
                if os.access(docker_hls_dir, os.W_OK):
                    self.base_dir = docker_hls_dir
                    logger.info(f"Using Docker container media/hls directory: {self.base_dir}")
                else:
                    logger.warning(f"Docker container media/hls directory is not writable: {docker_hls_dir}")
            except Exception as e:
                logger.warning(f"Error creating Docker container media/hls directory: {str(e)}")

        # If we still don't have a base_dir, use a temporary directory
        if not hasattr(self, 'base_dir'):
            try:
                self.base_dir = tempfile.mkdtemp(prefix="hls_")
                logger.warning(f"Using temporary directory for HLS files: {self.base_dir}")

                # Try to create a symbolic link from the expected directory to the temporary directory
                if self.expected_dir and platform.system() != 'Windows':
                    try:
                        # Create the parent directory if it doesn't exist
                        os.makedirs(os.path.dirname(self.expected_dir), exist_ok=True)

                        # Remove the existing directory or link if it exists
                        if os.path.exists(self.expected_dir):
                            if os.path.islink(self.expected_dir):
                                os.unlink(self.expected_dir)
                            else:
                                shutil.rmtree(self.expected_dir)

                        # Create the symbolic link
                        os.symlink(self.base_dir, self.expected_dir)
                        logger.info(f"Created symbolic link from {self.expected_dir} to {self.base_dir}")
                    except Exception as e:
                        logger.warning(f"Error creating symbolic link: {str(e)}")
            except Exception as e:
                # Last resort: use the current directory
                self.base_dir = os.getcwd()
                logger.error(f"Error creating temporary directory, using current directory: {self.base_dir}")

        self.base_url = settings.HLS_URL
        print(f"Using HLS directory: {self.base_dir}")

    def create(self, session_id=None):
        sid   = session_id or uuid.uuid4().hex
        path  = os.path.join(self.base_dir, sid)
        os.makedirs(path, exist_ok=True)

        # If we're using a temporary directory and couldn't create a symbolic link,
        # we need to make sure the files are accessible via the expected URL
        if self.expected_dir and self.base_dir != self.expected_dir and not os.path.islink(self.expected_dir):
            # Try to create a directory-specific symbolic link
            expected_session_dir = os.path.join(self.expected_dir, sid)
            try:
                # Create the parent directory if it doesn't exist
                if not os.path.exists(self.expected_dir):
                    os.makedirs(self.expected_dir, exist_ok=True)

                # Create a symbolic link for this specific session on Unix-like systems
                if platform.system() != 'Windows' and not os.path.exists(expected_session_dir):
                    os.symlink(path, expected_session_dir)
                    logger.info(f"Created session-specific symbolic link from {expected_session_dir} to {path}")
                # On Windows or if symlinks fail, set up a file copy mechanism
                elif not os.path.exists(expected_session_dir):
                    os.makedirs(expected_session_dir, exist_ok=True)
                    logger.info(f"Created session-specific directory: {expected_session_dir}")

                    # Set up a file watcher to copy files as they're created
                    import threading
                    def file_watcher():
                        import time
                        logger.info(f"Starting file watcher for {path} -> {expected_session_dir}")
                        error_count = 0
                        max_errors = 10  # Allow up to 10 errors before giving up

                        while error_count < max_errors:
                            try:
                                # Copy any new files from the source to the destination
                                for filename in os.listdir(path):
                                    src_file = os.path.join(path, filename)
                                    dst_file = os.path.join(expected_session_dir, filename)
                                    if os.path.isfile(src_file) and (not os.path.exists(dst_file) or 
                                                                    os.path.getmtime(src_file) > os.path.getmtime(dst_file)):
                                        shutil.copy2(src_file, dst_file)
                                        logger.info(f"Copied {src_file} to {dst_file}")

                                # Check if the playlist file exists and has been copied
                                playlist_file = os.path.join(path, "audio.m3u8")
                                if os.path.exists(playlist_file):
                                    dst_playlist = os.path.join(expected_session_dir, "audio.m3u8")
                                    if os.path.exists(dst_playlist):
                                        # If the playlist file exists and has been copied, we can reduce the check frequency
                                        time.sleep(2.0)  # Check less frequently once the playlist is available
                                    else:
                                        # If the playlist file exists but hasn't been copied, copy it immediately
                                        shutil.copy2(playlist_file, dst_playlist)
                                        logger.info(f"Copied playlist file to {dst_playlist}")
                                else:
                                    # If the playlist file doesn't exist yet, check more frequently
                                    time.sleep(0.5)

                                # Reset error count on successful iteration
                                error_count = 0
                            except Exception as e:
                                error_count += 1
                                logger.error(f"Error in file watcher ({error_count}/{max_errors}): {str(e)}")
                                time.sleep(1.0)  # Wait a bit longer after an error

                        logger.warning(f"File watcher for {path} -> {expected_session_dir} stopped after {max_errors} errors")

                    # Start the file watcher in a background thread
                    watcher_thread = threading.Thread(target=file_watcher, daemon=True)
                    watcher_thread.start()
            except Exception as e:
                logger.warning(f"Error creating session-specific directory or symlink: {str(e)}")

        return sid, path, f"{self.base_url}{sid}/audio.m3u8"

    def cleanup(self, path): shutil.rmtree(path, ignore_errors=True)
