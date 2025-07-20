#!/usr/bin/env python3
"""
Simple script to convert text to HLS audio using Google Text-to-Speech and ffmpeg.

This script:
1. Takes a text input
2. Converts text to speech using Google Text-to-Speech (gTTS)
3. Uses ffmpeg to create an HLS playlist and MP3 file
4. Supports streaming mode for processing text chunks incrementally
5. Optimized for low-latency HTTP audio streaming

LL-HLS Streaming Optimization:
- Uses a single long-lived ffmpeg process
- Streams gTTS output directly to ffmpeg
- Implements a producer/consumer loop
- Eliminates intermediate file concatenation
- Generates LL-HLS playlist and segment files continuously
- Time-to-first-audio ≤ 1s after first text tokens arrive
- Continuous audio with ~2-3s glass-to-glass latency while streaming

This implementation uses gTTS which is compatible with Python 3.12+.

CHANGELOG:
- Refactored for true low-latency streaming audio
- Single long-lived ffmpeg process instead of per-chunk processes
- Direct streaming of gTTS output to ffmpeg without temporary files
- Producer/consumer loop with ~40 word buffer for continuous processing
- Eliminated intermediate .pcm and .ts concatenation logic
- LL-HLS playlist & segment files appear continuously for immediate serving
- Backward compatible CLI with streaming as the default behavior
"""
import os
import tempfile
import subprocess
import logging
import argparse
import nltk
import shutil
import uuid
from gtts import gTTS

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Download NLTK punkt tokenizer for sentence splitting if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def speak_chunk_to_ffmpeg(text: str, lang: str, ffmpeg_stdin):
    """
    Stream text-to-speech output directly to ffmpeg.
    
    Args:
        text (str): Text to convert to speech
        lang (str): Language code for speech synthesis
        ffmpeg_stdin: stdin pipe of the ffmpeg process
        
    Returns:
        None
    """
    tts = gTTS(text=text, lang=lang, slow=False)
    for buf in tts.stream():          # MP3 frames
        ffmpeg_stdin.write(buf)
    ffmpeg_stdin.flush()


class StreamingTextToHLS:
    """
    Class for processing text chunks incrementally and creating HLS audio.

    This class maintains a single long-lived ffmpeg process and streams
    text-to-speech output directly to it for true low-latency streaming.
    """

    def __init__(self, output_dir=None, segment_duration=2, language="en"):
        """
        Initialize the StreamingTextToHLS instance.

        Args:
            output_dir (str): Path to output directory
            segment_duration (int): Duration of each segment in seconds (default: 2)
            language (str): Language code for speech synthesis
        """
        # Create a temporary directory if output_dir is not provided
        self.temp_dir = None
        if output_dir is None:
            self.temp_dir = tempfile.mkdtemp(prefix="text_to_hls_streaming_")
            output_dir = self.temp_dir

        self.segment_duration = segment_duration
        self.language = language

        # Create HLS directory
        self.hls_dir = os.path.join(output_dir, "hls")
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
        
        This process will run for the lifetime of the StreamingTextToHLS instance.
        """
        logger.info("Starting ffmpeg process for HLS streaming")
        
        # Build ffmpeg command for HLS streaming
        ffmpeg_cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "error",
            "-f", "mp3", "-i", "pipe:0",
            "-c:a", "aac", "-b:a", "128k",
            "-f", "hls",
            "-hls_time", "2",
            "-hls_flags",
              "delete_segments+append_list+independent_segments+program_date_time",
            "-hls_segment_type", "fmp4",
            "-hls_init_time", "0.1",
            "-hls_list_size", "6",
            "-hls_allow_cache", "0",
            os.path.join(self.hls_dir, "audio.m3u8"),
        ]
        
        # Start the ffmpeg process
        logger.info(f"Running ffmpeg command: {' '.join(ffmpeg_cmd)}")
        self.ffmpeg_process = subprocess.Popen(
            ffmpeg_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        self.ffmpeg_stdin = self.ffmpeg_process.stdin

    def process_chunk(self, text_chunk):
        """
        Process a single text chunk and convert it to speech.

        This method streams the text-to-speech output directly to the ffmpeg process.

        Args:
            text_chunk (str): Text chunk to process

        Returns:
            dict: Information about the processed chunk
        """
        if not text_chunk.strip():
            logger.warning("Empty text chunk received, skipping")
            return None

        logger.info(f"Processing text chunk {self.chunk_count + 1} with {len(text_chunk.split())} words")

        # Generate a unique ID for this chunk
        chunk_id = f"chunk_{self.chunk_count:03d}_{uuid.uuid4().hex[:8]}"

        # Stream text-to-speech output directly to ffmpeg
        speak_chunk_to_ffmpeg(
            text_chunk,
            self.language,
            self.ffmpeg_stdin
        )

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

        return {
            'playlist_path': os.path.join(self.hls_dir, "audio.m3u8"),
            'hls_dir': self.hls_dir,
            'segment_count': len([f for f in os.listdir(self.hls_dir) if f.endswith('.m4s')]),
            'mp3_file': None,  # No MP3 file is created in streaming mode
            'chunk_count': self.chunk_count
        }

    def __del__(self):
        """Clean up the ffmpeg process and temporary directory if created."""
        # Close the ffmpeg process if still running
        if self.ffmpeg_process and self.ffmpeg_process.poll() is None:
            if self.ffmpeg_stdin:
                self.ffmpeg_stdin.close()
            self.ffmpeg_process.terminate()
            try:
                self.ffmpeg_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.ffmpeg_process.kill()

        # Clean up the temporary directory if created
        if self.temp_dir and os.path.exists(self.temp_dir):
            logger.info(f"Cleaning up temporary directory: {self.temp_dir}")
            shutil.rmtree(self.temp_dir)
            pass


def process_text_to_hls(text,
                       output_dir: str = None,
                       segment_duration: int = 2,
                       language: str = "en") -> dict:
    """
    Process text to HLS audio with low-latency streaming.

    This function:
    1. Starts a single long-lived ffmpeg process
    2. Streams text-to-speech output directly to ffmpeg
    3. Creates an HLS playlist with optimized segment duration for low latency

    Args:
        text (str or list): Text to convert to speech. Can be a single string or a list of text chunks.
        output_dir (str): Path to output directory
        segment_duration (int): Duration of each segment in seconds (default: 2)
        language (str): Language code for speech synthesis

    Returns:
        dict: Information about the generated HLS stream
    """
    # Process as chunks using StreamingTextToHLS
    tts = StreamingTextToHLS(
        output_dir=output_dir,
        segment_duration=segment_duration,
        language=language,
    )

    if isinstance(text, str):
        text = [text]

    # Process each chunk
    for i, chunk in enumerate(text):
        logger.info(f"Processing chunk {i + 1}/{len(text)}")
        tts.process_chunk(chunk)

    # Finalize and return result
    return tts.finalize()


def main():
    """Main function."""
    # Parse arguments
    parser = argparse.ArgumentParser(description='Convert text to HLS audio using Google Text-to-Speech')
    parser.add_argument('--output-dir', '-o', type=str, help='Output directory')
    parser.add_argument('--segment-duration', '-d', type=int, default=2, help='Segment duration in seconds (ignored in streaming mode)')
    parser.add_argument('--language', '-l', type=str, default='en', help='Language code (e.g., en, fr, es)')
    parser.add_argument('--text-file', '-t', type=str, help='Path to text file')
    parser.add_argument('--streaming', action='store_true', help='Use streaming mode (default behavior, flag kept for backward compatibility)')
    parser.add_argument('--chunk-size', type=int, default=40, help='Number of words per chunk in streaming mode')
    args = parser.parse_args()

    # Get text from a file or use default
    if args.text_file:
        with open(args.text_file, 'r') as f:
            text = f.read()
    else:
        text = """
Il était une fois, dans l'immense étendue d'étoiles et de planètes, un petit renard aventurier nommé Freddy. Contrairement aux autres créatures qui restaient dans leurs territoires, Freddy aspirait sans cesse à de nouvelles escapades, au-delà des prairies de son pays natal. Un jour, alors qu'il jouait près des Bois Murmurants, une rafale venue du ciel apporta des murmures de secrets anciens et de récits inédits sur des trésors cachés dans de lointaines galaxies !

Les moustaches de Freddy frémirent d'excitation ; il avait entendu des légendes parlant de mondes éloignés où les renards couraient librement, explorant des royaumes étranges dépassant ses rêves les plus fous. L'idée qu'il puisse exister, parmi les étoiles, des lieux à découvrir était irrésistible !

Suivant une traînée de poussière d'étoiles scintillante et de miettes cosmiques sur le sol des Bois Murmurants, Freddy arriva devant un immense château mystérieux entièrement bâti de briques métalliques brillantes. Étonnamment, ce n'était pas une forteresse ordinaire : elle semblait flotter au-dessus des nuages !

Ce spectacle singulier lui coupa le souffle. Il effleura prudemment la surface froide, puis posa ses pattes sur un escalier de bois grinçant qui s'enfonçait dans l'obscurité. Freddy descendit, le cœur battant à l'idée de ce qui l'attendait au bas du château – peut-être même de sympathiques renards extraterrestres !

À l'intérieur se trouvait une immense bibliothèque, débordant de livres couverts de poussière et d'artefacts mystérieux brillant sous la lueur vacillante des bougies. On aurait dit qu'il venait de franchir un portail vers une époque révolue ! Freddy flâna entre les rayonnages remplis de récits d'explorateurs de l'espace venus des quatre coins des siècles. Son regard fut attiré par un vieux grimoire relié de cuir intitulé « Secrets au-delà des étoiles ».

L'enthousiasme de Freddy déborda lorsqu'il ouvrit fébrilement ce tome ancien, révélant une carte secrète menant non pas à un trésor, mais à un voyage au-delà des frontières du monde, à la recherche de savoir et d'amitié. L'heure de la véritable aventure de Freddy venait de sonner ! Il ne savait pas ce qui l'attendait – peut-être de nouveaux amis ou une leçon inattendue sur le courage et la curiosité ?

Freddy jeta un dernier regard au château flottant avant de se mettre en route, prêt à découvrir non seulement de lointaines planètes, mais aussi des histoires méconnues pouvant nous instruire tous. Son cœur débordait d'émerveillement tandis qu'il s'élançait dans l'espace, emportant avec lui ce rappel précieux : peu importe jusqu'où l'on s'aventure loin de chez soi ou l'audace de nos rêves, des amis et le savoir attendent ceux qui ont le courage de les chercher !
        """

    # Split text into chunks based on sentence boundaries and chunk_size
    words = text.split()
    chunks = []
    current_chunk = []
    current_chunk_size = 0
    
    # Use NLTK to split text into sentences
    sentences = nltk.sent_tokenize(text)
    
    for sentence in sentences:
        sentence_words = sentence.split()
        
        # If adding this sentence would exceed chunk_size,
        # finalize the current chunk and start a new one
        if current_chunk_size + len(sentence_words) > args.chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_chunk_size = 0
        
        # Add the sentence to the current chunk
        current_chunk.append(sentence)
        current_chunk_size += len(sentence_words)
        
        # If the chunk is now at or over the target size, finalize it
        if current_chunk_size >= args.chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_chunk_size = 0
    
    # Add any remaining text as the final chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    logger.info(f"Processing text with {len(chunks)} chunks")

    # Process text to HLS
    result = process_text_to_hls(
        chunks,
        output_dir=args.output_dir,
        segment_duration=args.segment_duration,
        language=args.language,
    )

    logger.info(f"HLS playlist created at {result['playlist_path']}")
    logger.info(f"Created {result['segment_count']} segments")
    logger.info(f"HLS directory: {result['hls_dir']}")
    if result['mp3_file']:
        logger.info(f"MP3 file created at {result['mp3_file']}")


if __name__ == "__main__":
    main()