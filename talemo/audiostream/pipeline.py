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
                        # Check if ffmpeg process is still running or stdin is closed
                        if (writer.ffmpeg_process is None or 
                            writer.ffmpeg_process.poll() is not None or 
                            writer.ffmpeg_stdin is None or 
                            writer.ffmpeg_stdin.closed):
                            logger.warning("ffmpeg process is not running or stdin is closed, restarting it")
                            writer._start_ffmpeg_process()

                            # Double-check that the process started successfully
                            if (writer.ffmpeg_process is None or 
                                writer.ffmpeg_process.poll() is not None or 
                                writer.ffmpeg_stdin is None or 
                                writer.ffmpeg_stdin.closed):
                                logger.error("Failed to restart ffmpeg process")
                                continue

                        # Process the text chunk
                        try:
                            tts.speak_chunk_to_ffmpeg(' '.join(buf), lang, writer.ffmpeg_stdin)
                            buf.clear()
                            progress_cb("chunk")
                            first_chunk = False
                        except Exception as e:
                            logger.error(f"Error in speak_chunk_to_ffmpeg: {str(e)}")
                            # Try to restart ffmpeg if there was an error
                            writer._start_ffmpeg_process()
                    except Exception as e:
                        logger.error(f"Error processing chunk: {str(e)}")
                        # Continue with the next chunk

            # Process any remaining text
            if buf:
                try:
                    # Check if ffmpeg process is still running or stdin is closed
                    if (writer.ffmpeg_process is None or 
                        writer.ffmpeg_process.poll() is not None or 
                        writer.ffmpeg_stdin is None or 
                        writer.ffmpeg_stdin.closed):
                        logger.warning("ffmpeg process is not running or stdin is closed, restarting it")
                        writer._start_ffmpeg_process()

                        # Double-check that the process started successfully
                        if (writer.ffmpeg_process is None or 
                            writer.ffmpeg_process.poll() is not None or 
                            writer.ffmpeg_stdin is None or 
                            writer.ffmpeg_stdin.closed):
                            logger.error("Failed to restart ffmpeg process for final chunk")
                            # Skip processing the final chunk
                            buf.clear()

                    # Process the remaining text
                    try:
                        tts.speak_chunk_to_ffmpeg(' '.join(buf), lang, writer.ffmpeg_stdin)
                        buf.clear()
                    except Exception as e:
                        logger.error(f"Error in speak_chunk_to_ffmpeg for final chunk: {str(e)}")
                        # Try to restart ffmpeg if there was an error
                        writer._start_ffmpeg_process()
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
