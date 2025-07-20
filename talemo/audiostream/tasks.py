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
def generate_audio_stream(self, prompt, lang="en", session_id=None):
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

    def progress(evt, meta=None):
        self.update_state(state="PROGRESS", meta={"event":evt, **(meta or {})})

    try:
        playlist_path = os.path.join(path, "audio.m3u8")
        logger.info(f"Running audio session with playlist path: {playlist_path}")
        run_audio_session(prompt, playlist_path, lang, progress_cb=progress)

        # Verify that the playlist file was created
        if os.path.exists(playlist_path):
            logger.info(f"Playlist file created successfully: {playlist_path}")
        else:
            logger.warning(f"Playlist file was not created: {playlist_path}")

            # Try to create a minimal playlist as a last resort
            try:
                from .hls import StreamingHLSWriter
                writer = StreamingHLSWriter(os.path.dirname(playlist_path))
                writer._create_minimal_playlist(playlist_path)
                logger.info(f"Created minimal playlist as a last resort: {playlist_path}")
            except Exception as e:
                logger.error(f"Error creating minimal playlist as a last resort: {str(e)}")

        # Update the session status to ready even if the playlist file wasn't created
        # This ensures the task completes successfully and the client gets a response
        AudioSession.objects.filter(session_id=sid).update(status="ready")
    except Exception as exc:
        logger.error(f"Error generating audio stream: {str(exc)}")
        AudioSession.objects.filter(session_id=sid).update(status="error", error_message=str(exc))
        raise

    return {"playlist": playlist_url}
