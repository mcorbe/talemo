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
        chunk_count = 0
        
        # Create a text log file to store all text chunks
        text_log_path = os.path.join(output_dir, "text_chunks.log")
        
        # Write the initial prompt to the log file
        with open(text_log_path, 'w', encoding='utf-8') as f:
            f.write(f"=== Audio Generation Session ===\n")
            f.write(f"Timestamp: {os.popen('date').read().strip()}\n")
            f.write(f"Original prompt: {prompt}\n")
            f.write(f"Language: {lang}\n")
            f.write(f"Chunk words: {chunk_words}\n")
            f.write(f"Output directory: {output_dir}\n")
            f.write(f"\n=== Text Chunks ===\n\n")
        
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
                            text_chunk = ' '.join(buf)
                            chunk_count += 1
                            
                            # Log to console
                            logger.info(f"Sending text chunk #{chunk_count} to TTS: '{text_chunk}'")
                            
                            # Write to file
                            with open(text_log_path, 'a', encoding='utf-8') as f:
                                f.write(f"=== Chunk #{chunk_count} ===\n")
                                f.write(f"{text_chunk}\n\n")
                            
                            tts.speak_chunk_to_ffmpeg(text_chunk, lang, writer.ffmpeg_stdin)
                            buf.clear()
                            progress_cb("chunk", {"chunk_count": chunk_count})
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
                        text_chunk = ' '.join(buf)
                        chunk_count += 1
                        
                        # Log to console
                        logger.info(f"Sending final text chunk #{chunk_count} to TTS: '{text_chunk}'")
                        
                        # Write to file
                        with open(text_log_path, 'a', encoding='utf-8') as f:
                            f.write(f"=== Final Chunk #{chunk_count} ===\n")
                            f.write(f"{text_chunk}\n\n")
                        
                        tts.speak_chunk_to_ffmpeg(text_chunk, lang, writer.ffmpeg_stdin)
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
                logger.warning(f"Playlist file still not created after finalize: {local_playlist_path}, which is unexpected with FFmpeg temp_file flag")

            # Write summary to the log file
            with open(text_log_path, 'a', encoding='utf-8') as f:
                f.write(f"\n=== Summary ===\n")
                f.write(f"Total chunks processed: {chunk_count}\n")
                f.write(f"Session completed at: {os.popen('date').read().strip()}\n")
                f.write(f"Playlist path: {playlist_path}\n")

            return info
        except Exception as e:
            logger.error(f"Error finalizing HLS playlist: {str(e)}")

            # Check if the playlist file exists after finalize error
            local_playlist_path = os.path.join(output_dir, "audio.m3u8")
            if not os.path.exists(local_playlist_path):
                logger.warning(f"Playlist file not found after finalize error: {local_playlist_path}, which is unexpected with FFmpeg temp_file flag")

            return {"error": str(e), "playlist_path": os.path.join(output_dir, "audio.m3u8")}

    return asyncio.run(_run())
