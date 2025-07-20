import asyncio, os
import logging
from .hls import StreamingHLSWriter
from . import tts, llm

logger = logging.getLogger(__name__)

def run_audio_session(prompt, playlist_path, lang="en", chunk_words=40,
                      progress_cb=lambda *a,**k: None):

    async def _run():
        # Extract the directory path from the playlist_path
        output_dir = os.path.dirname(playlist_path)
        writer = StreamingHLSWriter(output_dir)
        buf = []
        first_chunk = True
        try:
            async for tok in llm.stream_tokens(prompt):
                buf.append(tok)
                # Use a smaller chunk size for the first chunk to start audio faster
                if tok.endswith(('.', '!', '?')) or (first_chunk and len(buf) >= 10) or len(buf) >= chunk_words:
                    try:
                        # Check if ffmpeg process is still running
                        if writer.ffmpeg_process is None or writer.ffmpeg_process.poll() is not None:
                            logger.warning("ffmpeg process is not running, restarting it")
                            writer._start_ffmpeg_process()

                        # Process the text chunk
                        if writer.ffmpeg_stdin and not writer.ffmpeg_stdin.closed:
                            tts.speak_chunk_to_ffmpeg(' '.join(buf), lang, writer.ffmpeg_stdin)
                            buf.clear()
                            progress_cb("chunk")
                            first_chunk = False
                        else:
                            logger.warning("Cannot process chunk: ffmpeg stdin is closed or None")
                    except Exception as e:
                        logger.error(f"Error processing chunk: {str(e)}")
                        # Continue with the next chunk

            # Process any remaining text
            if buf:
                try:
                    # Check if ffmpeg process is still running
                    if writer.ffmpeg_process is None or writer.ffmpeg_process.poll() is not None:
                        logger.warning("ffmpeg process is not running, restarting it")
                        writer._start_ffmpeg_process()

                    # Process the remaining text
                    if writer.ffmpeg_stdin and not writer.ffmpeg_stdin.closed:
                        tts.speak_chunk_to_ffmpeg(' '.join(buf), lang, writer.ffmpeg_stdin)
                    else:
                        logger.warning("Cannot process final chunk: ffmpeg stdin is closed or None")
                except Exception as e:
                    logger.error(f"Error processing final chunk: {str(e)}")
        except Exception as e:
            logger.error(f"Error in stream_tokens: {str(e)}")

        # Finalize the HLS playlist
        try:
            info = writer.finalize()
            progress_cb("done", info)

            # Verify that the playlist file exists
            local_playlist_path = os.path.join(output_dir, "audio.m3u8")
            if not os.path.exists(local_playlist_path):
                logger.warning(f"Playlist file still not created after finalize: {local_playlist_path}")
                # Create a minimal playlist as a last resort
                writer._create_minimal_playlist(local_playlist_path)

            return info
        except Exception as e:
            logger.error(f"Error finalizing HLS playlist: {str(e)}")

            # Try to create a minimal playlist even if finalize fails
            try:
                local_playlist_path = os.path.join(output_dir, "audio.m3u8")
                if not os.path.exists(local_playlist_path):
                    logger.warning(f"Creating minimal playlist after finalize error: {local_playlist_path}")
                    writer._create_minimal_playlist(local_playlist_path)
            except Exception as inner_e:
                logger.error(f"Error creating minimal playlist after finalize error: {str(inner_e)}")

            return {"error": str(e), "playlist_path": os.path.join(output_dir, "audio.m3u8")}

    return asyncio.run(_run())
