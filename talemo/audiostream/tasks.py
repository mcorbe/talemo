from celery import shared_task
from .models import AudioSession
from .storage import SegmentStore
from .pipeline import run_audio_session
import os
import logging
import traceback
import sys

# Configure logging
logger = logging.getLogger(__name__)
# Ensure logs are printed to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

@shared_task(bind=True)
def generate_audio_stream(self, prompt, lang="en", session_id=None,
                          min_segments_before_return=1,
                          timeout_before_return=5.0):
    """
    Generate an audio stream from the given prompt.

    Args:
        prompt (str): The text prompt to generate audio from
        lang (str): The language code (default: "en")
        session_id (str, optional): A custom session ID
        min_segments_before_return (int): Minimum number of segments to wait for before returning (default: 1)
        timeout_before_return (float): Maximum time to wait for segments in seconds (default: 5.0)

    Returns:
        dict: A dictionary containing the playlist URL
    """
    logger.info(f"generate_audio_stream task started with prompt: {prompt}, lang: {lang}, session_id: {session_id}")
    logger.info(f"Task ID: {self.request.id}")

    try:
        logger.info(f"Task queue: {self.request.delivery_info.get('routing_key', 'unknown')}")
    except Exception as e:
        logger.warning(f"Could not get routing key: {str(e)}")

    store = SegmentStore()
    sid, path, playlist_url = store.create(session_id)

    # Log the path where files will be stored
    logger.info(f"HLS files will be stored at: {path}")
    logger.info(f"HLS playlist URL: {playlist_url}")

    AudioSession.objects.update_or_create(
        session_id=sid,
        defaults={"status":"running","playlist_rel_url":playlist_url},
    )

    # FFmpeg will create the playlist with the temp_file flag
    playlist_path = os.path.join(path, "audio.m3u8")
    from .hls import StreamingHLSWriter
    writer = StreamingHLSWriter(path)

    # Verify that the playlist file is created by FFmpeg
    # It might take a moment for FFmpeg to create the file
    import time
    start_time = time.time()
    while not os.path.exists(playlist_path) and time.time() - start_time < 1.0:
        time.sleep(0.1)  # Short sleep to allow FFmpeg to create the file

    if os.path.exists(playlist_path):
        logger.info(f"FFmpeg created playlist file successfully: {playlist_path}")
    else:
        logger.warning(f"Playlist file not created by FFmpeg yet: {playlist_path}, which is unexpected with temp_file flag")

    def progress(evt, meta=None):
        self.update_state(state="PROGRESS", meta={"event":evt, **(meta or {})})

    # 2. Start the actual rendering pipeline in the background
    import threading

    def _render():
        try:
            logger.info(f"Running audio session with playlist path: {playlist_path}")
            run_audio_session(prompt, playlist_path, lang, progress_cb=progress)

            # Update the session status to ready when processing is complete
            AudioSession.objects.filter(session_id=sid).update(status="ready")
        except Exception as exc:
            logger.error(f"Error generating audio stream: {str(exc)}")
            AudioSession.objects.filter(session_id=sid).update(status="error", error_message=str(exc))

    # Start the audio processing thread
    t = threading.Thread(target=_render, daemon=True, name=f"HLS-{sid}")
    t.start()

    # 3. Poll until the first N segments are present (or we time-out)
    expected_first_segment = os.path.join(path, f"segment_000.m4s")
    deadline = time.time() + timeout_before_return

    # Use contextlib.suppress to avoid a race condition when the directory disappears
    from contextlib import suppress

    while time.time() < deadline:
        with suppress(FileNotFoundError):
            if os.path.exists(expected_first_segment):
                logger.info(f"First segment found: {expected_first_segment}")
                break
        time.sleep(0.05)  # 50 ms polling interval
    else:
        logger.warning(f"Timeout waiting for first segment after {timeout_before_return}s")

    # 4. Mark DB as 'ready' and return immediately - ffmpeg is still running
    AudioSession.objects.filter(session_id=sid).update(status="ready")
    return {"playlist": playlist_url}
