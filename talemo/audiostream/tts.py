from gtts import gTTS
import logging

logger = logging.getLogger(__name__)

def speak_chunk_to_ffmpeg(text: str, lang: str, ffmpeg_stdin):
    if ffmpeg_stdin.closed:
        logger.error("Cannot write to ffmpeg: stdin is closed")
        return

    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        for buf in tts.stream():
            ffmpeg_stdin.write(buf)
        ffmpeg_stdin.flush()
    except BrokenPipeError:
        logger.error("BrokenPipeError: ffmpeg process may have terminated unexpectedly")
        # Don't re-raise the exception, just log it and continue
    except Exception as e:
        logger.error(f"Error in speak_chunk_to_ffmpeg: {str(e)}")
        # Don't re-raise other exceptions either, just log them
