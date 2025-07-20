import os
from django.apps import AppConfig
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class AudiostreamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'talemo.audiostream'

    def ready(self):
        # Create the media/hls directory if it doesn't exist
        if hasattr(settings, 'MEDIA_ROOT'):
            hls_dir = os.path.join(settings.MEDIA_ROOT, 'hls')
            os.makedirs(hls_dir, exist_ok=True)
            logger.info(f"Ensured HLS directory exists: {hls_dir}")

        # Also try to create the Docker container path
        docker_hls_dir = "/app/media/hls"
        try:
            os.makedirs(docker_hls_dir, exist_ok=True)
            logger.info(f"Ensured Docker container HLS directory exists: {docker_hls_dir}")
        except Exception as e:
            logger.warning(f"Could not create Docker container HLS directory: {str(e)}")
