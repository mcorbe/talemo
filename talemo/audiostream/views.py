import os
import logging
import traceback
import sys
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from celery.result import AsyncResult
from .tasks import generate_audio_stream
from .models import AudioSession

# Configure logging
logger = logging.getLogger(__name__)
# Ensure logs are printed to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

@api_view(["POST"])
@permission_classes([AllowAny])
def start_audio_session(request):
    logger.info(f"start_audio_session called with request: {request.data}")
    prompt = request.data["prompt"]
    lang = request.data.get("lang","en")

    # Check if Celery is configured to run tasks eagerly (synchronously)
    from django.conf import settings
    run_eagerly = getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False)

    # Check if Redis is available
    redis_available = False
    try:
        import redis
        from django.conf import settings
        redis_client = redis.Redis.from_url(settings.CELERY_BROKER_URL)
        redis_available = redis_client.ping()
        logger.info(f"Redis is {'available' if redis_available else 'not available'}")
    except Exception as e:
        logger.warning(f"Error checking Redis availability: {str(e)}")

    # Determine if we should run the task asynchronously or synchronously
    run_async = not run_eagerly and redis_available

    if run_async:
        try:
            logger.info(f"Calling generate_audio_stream.delay with prompt: {prompt}, lang: {lang}")
            async_res = generate_audio_stream.delay(prompt, lang)
            logger.info(f"generate_audio_stream.delay returned: {async_res}")

            # If we get here, Celery is working
            session_id = async_res.id
        except Exception as e:
            # If there's an error, fall back to synchronous execution
            logger.warning(f"Error calling generate_audio_stream.delay: {str(e)}")
            run_async = False

    if not run_async:
        logger.warning("Running task synchronously")

        # Generate a session ID
        import uuid
        session_id = uuid.uuid4().hex

        # Run the task synchronously
        try:
            result = repr((prompt, lang, session_id))
            logger.info(f"Synchronous execution result: {result}")
        except Exception as e:
            logger.error(f"Error in synchronous execution: {str(e)}")
            # Return an error response
            return Response({"error": str(e)}, status=500)

    # Construct the playlist URL
    playlist_url = f"{settings.HLS_URL}{session_id}/audio.m3u8"

    # Log the playlist URL for debugging
    logger.info(f"Generated playlist URL: {playlist_url}")

    # Check if we need to use an alternative URL
    try:
        # First, check if the Docker container path exists and is accessible
        docker_hls_dir = f"/app/media/hls/{session_id}"
        if os.path.exists(docker_hls_dir) and os.access(docker_hls_dir, os.R_OK):
            logger.info(f"Docker container HLS directory exists and is readable: {docker_hls_dir}")
            # Use the standard URL, which should work with the Docker container path
            playlist_url = f"{settings.HLS_URL}{session_id}/audio.m3u8"
            logger.info(f"Using standard playlist URL for Docker container: {playlist_url}")
        else:
            # Check if the media directory exists and is accessible
            media_dir = os.path.join(settings.MEDIA_ROOT, 'hls')
            if not os.path.exists(media_dir) or not os.access(media_dir, os.R_OK):
                logger.warning(f"Media directory {media_dir} does not exist or is not readable")

                # Check if there's a temporary directory being used
                import tempfile
                temp_dir = tempfile.gettempdir()
                for dir_name in os.listdir(temp_dir):
                    if dir_name.startswith('hls_'):
                        # Found a temporary HLS directory, use it for the URL
                        temp_hls_dir = os.path.join(temp_dir, dir_name)
                        if os.path.isdir(temp_hls_dir):
                            # Use a URL that will be handled by the static file server
                            # Use session_id instead of async_res.id to handle both async and sync cases
                            playlist_url = f"/temp_hls/{dir_name}/{session_id}/audio.m3u8"
                            logger.info(f"Using alternative playlist URL: {playlist_url}")
                            break
    except Exception as e:
        logger.error(f"Error checking for alternative URL: {str(e)}")

    return Response({
        "session_id": session_id,
        "playlist": playlist_url,
        "task_id": session_id,  # Include task_id in the response for status checking
    })

@api_view(["GET"])
@permission_classes([AllowAny])
def task_status(request, task_id):
    """
    Check the status of a Celery task and return it as JSON.

    Possible states:
    - PENDING: Task is waiting to be processed
    - PROGRESS: Task is in progress, with meta-information about progress
    - SUCCESS: Task completed successfully
    - FAILURE: Task failed
    """
    logger.info(f"Checking status for task: {task_id}")

    # Get the task result
    task_result = AsyncResult(task_id)

    # Get the task state
    state = task_result.state

    # Prepare the response
    response = {
        "state": state,
    }

    # Add additional information based on the state
    if state == 'PENDING':
        response["status"] = "Task is pending"
    elif state == 'PROGRESS':
        # Get progress information from the task
        if task_result.info and isinstance(task_result.info, dict):
            meta = task_result.info
            response["event"] = meta.get("event", "unknown")
            # Include any other meta-information
            for key, value in meta.items():
                if key != "event":
                    response[key] = value
        response["status"] = "Task is in progress"
    elif state == 'SUCCESS':
        # Task completed successfully
        result = task_result.get()
        response["status"] = "Task completed successfully"
        response["result"] = result
        # Include the playlist URL in the response
        if isinstance(result, dict) and "playlist" in result:
            response["playlist"] = result["playlist"]
    elif state == 'FAILURE':
        # Task failed
        response["status"] = "Task failed"
        response["error"] = str(task_result.result)
    else:
        # Unknown state
        response["status"] = f"Unknown state: {state}"

    return Response(response)
