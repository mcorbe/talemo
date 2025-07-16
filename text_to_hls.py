#!/usr/bin/env python3
"""
Simple script to convert text to HLS audio using Google Text-to-Speech and ffmpeg.

This script:
1. Takes a text input
2. Converts text to speech using Google Text-to-Speech (gTTS)
3. Uses ffmpeg to create an HLS playlist and MP3 file
4. Supports streaming mode for processing text chunks incrementally

This implementation uses gTTS which is compatible with Python 3.12+.
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



def create_mp3_file(input_file, output_file):
    """
    Create an MP3 file from a PCM audio file using ffmpeg.

    Args:
        input_file (str): Path to input PCM file
        output_file (str): Path to output MP3 file

    Returns:
        str: Path to output MP3 file
    """
    logger.info(f"Creating MP3 file from {input_file}")

    # Build ffmpeg command
    ffmpeg_cmd = [
        'ffmpeg',
        '-f', 's16le',  # Input format: signed 16-bit little-endian
        '-ar', '24000',  # Sample rate: 24kHz
        '-ac', '1',  # Channels: mono
        '-i', input_file,  # Input file

        # MP3 output
        '-c:a', 'libmp3lame',  # Audio codec: MP3
        '-b:a', '128k',  # Bitrate: 128kbps
        '-f', 'mp3',  # Format: MP3
        '-y',  # Overwrite an output file if it exists
        output_file  # Output file
    ]

    # Run ffmpeg
    logger.info(f"Running ffmpeg command: {' '.join(ffmpeg_cmd)}")
    try:
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        logger.info(f"MP3 file created at {output_file}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error creating MP3 file: {e}")


class StreamingTextToHLS:
    """
    Class for processing text chunks incrementally and creating HLS audio.

    This class maintains state between chunk processing and updates the HLS playlist
    as new chunks arrive.
    """

    def __init__(self, output_dir=None, segment_duration=2, language="en"):
        """
        Initialize the StreamingTextToHLS instance.

        Args:
            output_dir (str): Path to output directory
            segment_duration (int): Duration of each segment in seconds
            language (str): Language code for speech synthesis
            speaker_embedding (str): Path to speaker embedding file (not used with gTTS)
        """
        # Create temporary directory if output_dir is not provided
        self.temp_dir = None
        if output_dir is None:
            self.temp_dir = tempfile.mkdtemp(prefix="text_to_hls_streaming_")
            output_dir = self.temp_dir

        self.output_dir = output_dir
        self.segment_duration = segment_duration
        self.language = language

        # Create subdirectories
        self.pcm_dir = os.path.join(output_dir, "pcm")
        self.hls_dir = os.path.join(output_dir, "hls")
        self.mp3_dir = os.path.join(output_dir, "mp3")
        os.makedirs(self.pcm_dir, exist_ok=True)
        os.makedirs(self.hls_dir, exist_ok=True)
        os.makedirs(self.mp3_dir, exist_ok=True)

        # Initialize state
        self.chunk_count = 0
        self.segment_count = 0
        self.playlist_path = os.path.join(self.hls_dir, "playlist.m3u8")
        self.mp3_file = os.path.join(self.mp3_dir, "audio.mp3")
        self.pcm_files = []

        # Initialize playlist with header if it doesn't exist
        if not os.path.exists(self.playlist_path):
            with open(self.playlist_path, 'w') as f:
                f.write("#EXTM3U\n")
                f.write("#EXT-X-VERSION:3\n")
                f.write(f"#EXT-X-TARGETDURATION:{segment_duration}\n")
                f.write("#EXT-X-MEDIA-SEQUENCE:0\n")

    def text_chunk_to_speech(self, text_chunk, output_file, language=None):
        """
        Convert text to speech using Google Text-to-Speech (gTTS).

        This function:
        1. Uses gTTS to convert text to speech
        2. Streams the audio data directly to ffmpeg for PCM conversion
        3. No temporary MP3 file is created

        Args:
            text_chunk (str): Text to convert to speech
            output_file (str): Path to output PCM file
            language (str): Language code for speech synthesis

        Returns:
            str: Path to output a PCM file
        """
        if language is None:
            language = self.language

        logger.info(f"Converting text to speech using gTTS: {text_chunk[:50]}...")

        # Create gTTS object
        tts = gTTS(text=text_chunk, lang=language, slow=False)

        # Set up the ffmpeg command to read from stdin
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', 'pipe:0',  # Read from stdin
            '-f', 's16le',  # Output format: signed 16-bit little-endian
            '-acodec', 'pcm_s16le',  # Audio codec
            '-ar', '24000',  # Sample rate: 24kHz
            '-ac', '1',  # Channels: mono
            '-y',  # Overwrite an output file if it exists
            output_file  # Output PCM file
        ]

        # Start the ffmpeg process
        logger.info(f"Starting ffmpeg process to convert speech to PCM format")
        ffmpeg_process = subprocess.Popen(
            ffmpeg_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Stream audio data to ffmpeg
        try:
            for audio_chunk in tts.stream():
                ffmpeg_process.stdin.write(audio_chunk)

            # Close stdin to signal end of input
            ffmpeg_process.stdin.close()

            # Wait for ffmpeg to finish
            ffmpeg_process.wait()

            if ffmpeg_process.returncode != 0:
                logger.error(f"ffmpeg process returned non-zero exit code: {ffmpeg_process.returncode}")
                raise subprocess.CalledProcessError(ffmpeg_process.returncode, ffmpeg_cmd)

        except Exception as e:
            logger.error(f"Error streaming audio to ffmpeg: {e}")
            # Kill ffmpeg process if it's still running
            if ffmpeg_process.poll() is None:
                ffmpeg_process.kill()
            raise

        logger.info(f"Converted speech to PCM format at {output_file}")
        return output_file

    # def create_hls_playlist(self, input_file, output_dir, segment_duration=None):
    #     """
    #     Create HLS playlist from PCM audio file using ffmpeg.
    #
    #     Args:
    #         input_file (str): Path to input PCM file
    #         output_dir (str): Path to output directory
    #         segment_duration (int): Duration of each segment in seconds
    #
    #     Returns:
    #         str: Path to HLS playlist
    #     """
    #     if segment_duration is None:
    #         segment_duration = self.segment_duration
    #
    #     logger.info(f"Creating HLS playlist from {input_file}")
    #
    #     # Create an output directory
    #     os.makedirs(output_dir, exist_ok=True)
    #
    #     # Set paths
    #     playlist_path = os.path.join(output_dir, "playlist.m3u8")
    #     segment_pattern = os.path.join(output_dir, "segment_%03d.ts")
    #
    #     # Build ffmpeg command
    #     ffmpeg_cmd = [
    #         'ffmpeg',
    #         '-f', 's16le',  # Input format: signed 16-bit little-endian
    #         '-ar', '24000',  # Sample rate: 24kHz (XTTS-v2 output rate)
    #         '-ac', '1',  # Channels: mono
    #         '-i', input_file,  # Input file
    #
    #         # HLS output
    #         '-c:a', 'aac',  # Audio codec: AAC
    #         '-b:a', '128k',  # Bitrate: 128kbps
    #         '-f', 'hls',  # Format: HLS
    #         '-hls_time', str(segment_duration),  # Segment duration
    #         '-hls_list_size', '0',  # Include all segments in playlist
    #         '-hls_segment_type', 'mpegts',  # Segment type: MPEG-TS
    #         '-hls_segment_filename', segment_pattern,  # Segment filename pattern
    #         playlist_path  # Playlist path
    #     ]
    #
    #     # Run ffmpeg
    #     logger.info(f"Running ffmpeg command: {' '.join(ffmpeg_cmd)}")
    #     subprocess.run(ffmpeg_cmd, check=True)
    #
    #     logger.info(f"HLS playlist created at {playlist_path}")
    #     return playlist_path

    def process_chunk(self, text_chunk):
        """
        Process a single text chunk and add it to the HLS playlist.

        Args:
            text_chunk (str): Text chunk to process

        Returns:
            dict: Information about the processed chunk
        """
        if not text_chunk.strip():
            logger.warning("Empty text chunk received, skipping")
            return None

        logger.info(f"Processing text chunk {self.chunk_count + 1} with {len(text_chunk.split())} words")

        # Generate a unique filename for this chunk
        chunk_id = f"chunk_{self.chunk_count:03d}_{uuid.uuid4().hex[:8]}"
        pcm_file = os.path.join(self.pcm_dir, f"{chunk_id}.pcm")

        # Convert text chunk to speech
        self.text_chunk_to_speech(
            text_chunk,
            pcm_file,
            language=self.language,
        )

        # Add to a list of PCM files
        self.pcm_files.append(pcm_file)

        # Create HLS segments for this chunk
        segment_pattern = os.path.join(self.hls_dir, f"{chunk_id}_segment_%03d.ts")

        # Build ffmpeg command for HLS segments
        ffmpeg_cmd = [
            'ffmpeg',
            '-f', 's16le',  # Input format: signed 16-bit little-endian
            '-ar', '24000',  # Sample rate: 24kHz
            '-ac', '1',  # Channels: mono
            '-i', pcm_file,  # Input file

            # HLS output
            '-c:a', 'aac',  # Audio codec: AAC
            '-b:a', '128k',  # Bitrate: 128kbps
            '-f', 'segment',  # Format: segment
            '-segment_time', str(self.segment_duration),  # Segment duration
            '-segment_format', 'mpegts',  # Segment format: MPEG-TS
            '-segment_list', f"{self.hls_dir}/{chunk_id}_segments.m3u8",  # Temporary segment list
            '-y',  # Overwrite output files if they exist
            segment_pattern  # Segment filename pattern
        ]

        # Run ffmpeg
        logger.info(f"Running ffmpeg command for chunk {self.chunk_count + 1}")
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Count new segments
        new_segments = [f for f in os.listdir(self.hls_dir) if
                        f.startswith(f"{chunk_id}_segment_") and f.endswith('.ts')]
        new_segments.sort()

        # Update the main playlist
        with open(self.playlist_path, 'a') as main_playlist:
            for segment in new_segments:
                main_playlist.write(f"#EXTINF:{self.segment_duration}.0,\n")
                main_playlist.write(f"{segment}\n")

        # Update state
        self.chunk_count += 1
        self.segment_count += len(new_segments)

        return {
            'chunk_id': chunk_id,
            'pcm_file': pcm_file,
            'segment_count': len(new_segments),
            'total_segments': self.segment_count
        }

    def finalize(self):
        """
        Finalize the HLS playlist and create a combined MP3 file.

        Returns:
            dict: Information about the generated HLS stream and MP3 file
        """
        logger.info("Finalizing HLS playlist and creating MP3 file")

        # Add end marker to the playlist
        with open(self.playlist_path, 'a') as f:
            f.write("#EXT-X-ENDLIST\n")

        # Create a combined MP3 file if there are PCM files
        if self.pcm_files:
            # Concatenate PCM files directly (PCM is a headerless format)
            concat_pcm = os.path.join(self.pcm_dir, "combined_audio.pcm")

            logger.info("Concatenating PCM files directly")
            try:
                with open(concat_pcm, 'wb') as outfile:
                    for pcm_file in self.pcm_files:
                        with open(pcm_file, 'rb') as infile:
                            # Copy the content of each PCM file to the output file
                            shutil.copyfileobj(infile, outfile)

                # Create an MP3 file from the concatenated PCM
                create_mp3_file(concat_pcm, self.mp3_file)

            except Exception as e:
                logger.error(f"Error concatenating PCM files or creating MP3: {e}")

        return {
            'playlist_path': self.playlist_path,
            'hls_dir': self.hls_dir,
            'segment_count': self.segment_count,
            'mp3_file': self.mp3_file,
            'chunk_count': self.chunk_count
        }

    def __del__(self):
        """Clean up temporary directory if created."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            logger.info(f"Cleaning up temporary directory: {self.temp_dir}")
            # Uncomment to enable cleanup
            # shutil.rmtree(self.temp_dir)
            pass


def process_chunks_to_hls(text: list,
                          output_dir: str = None,
                          segment_duration: int = 2,
                          language: str = "en") -> dict:
    """
    Process text to HLS audio and MP3 file.

    This function:
    1. Converts text to speech using Google Text-to-Speech (gTTS)
    2. Creates an HLS playlist from the audio
    3. Creates an MP3 file from the audio

    Args:
        text (str or list): Text to convert to speech. Can be a single string or a list of text chunks.
        output_dir (str): Path to output directory
        segment_duration (int): Duration of each segment in seconds
        language (str): Language code for speech synthesis

    Returns:
        dict: Information about the generated HLS stream and MP3 file
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
    parser.add_argument('--segment-duration', '-d', type=int, default=2, help='Segment duration in seconds')
    parser.add_argument('--language', '-l', type=str, default='en', help='Language code (e.g., en, fr, es)')
    parser.add_argument('--text-file', '-t', type=str, help='Path to text file')
    parser.add_argument('--streaming', action='store_true', help='Use streaming mode to process text in chunks')
    parser.add_argument('--chunk-size', type=int, default=200, help='Number of words per chunk in streaming mode')
    args = parser.parse_args()

    # Get text from a file or use default
    if args.text_file:
        with open(args.text_file, 'r') as f:
            text = f.read()
    else:
        text = """
Il était une fois, dans l’immense étendue d’étoiles et de planètes, un petit renard aventurier nommé Freddy. Contrairement aux autres créatures qui restaient dans leurs territoires, Freddy aspirait sans cesse à de nouvelles escapades, au-delà des prairies de son pays natal. Un jour, alors qu’il jouait près des Bois Murmurants, une rafale venue du ciel apporta des murmures de secrets anciens et de récits inédits sur des trésors cachés dans de lointaines galaxies !

Les moustaches de Freddy frémirent d’excitation ; il avait entendu des légendes parlant de mondes éloignés où les renards couraient librement, explorant des royaumes étranges dépassant ses rêves les plus fous. L’idée qu’il puisse exister, parmi les étoiles, des lieux à découvrir était irrésistible !

Suivant une traînée de poussière d’étoiles scintillante et de miettes cosmiques sur le sol des Bois Murmurants, Freddy arriva devant un immense château mystérieux entièrement bâti de briques métalliques brillantes. Étonnamment, ce n’était pas une forteresse ordinaire : elle semblait flotter au-dessus des nuages !

Ce spectacle singulier lui coupa le souffle. Il effleura prudemment la surface froide, puis posa ses pattes sur un escalier de bois grinçant qui s’enfonçait dans l’obscurité. Freddy descendit, le cœur battant à l’idée de ce qui l’attendait au bas du château – peut-être même de sympathiques renards extraterrestres !

À l’intérieur se trouvait une immense bibliothèque, débordant de livres couverts de poussière et d’artefacts mystérieux brillant sous la lueur vacillante des bougies. On aurait dit qu’il venait de franchir un portail vers une époque révolue ! Freddy flâna entre les rayonnages remplis de récits d’explorateurs de l’espace venus des quatre coins des siècles. Son regard fut attiré par un vieux grimoire relié de cuir intitulé « Secrets au-delà des étoiles ».

L’enthousiasme de Freddy déborda lorsqu’il ouvrit fébrilement ce tome ancien, révélant une carte secrète menant non pas à un trésor, mais à un voyage au-delà des frontières du monde, à la recherche de savoir et d’amitié. L’heure de la véritable aventure de Freddy venait de sonner ! Il ne savait pas ce qui l’attendait – peut-être de nouveaux amis ou une leçon inattendue sur le courage et la curiosité ?

Freddy jeta un dernier regard au château flottant avant de se mettre en route, prêt à découvrir non seulement de lointaines planètes, mais aussi des histoires méconnues pouvant nous instruire tous. Son cœur débordait d’émerveillement tandis qu’il s’élançait dans l’espace, emportant avec lui ce rappel précieux : peu importe jusqu’où l’on s’aventure loin de chez soi ou l’audace de nos rêves, des amis et le savoir attendent ceux qui ont le courage de les chercher !
        """

    chunks = [text]

    # Process text to HLS
    if args.streaming:
        # Split text into chunks based on chunk_size
        words = text.split()
        chunks = []
        for i in range(0, len(words), args.chunk_size):
            chunk = ' '.join(words[i:i + args.chunk_size])
            chunks.append(chunk)

        logger.info(f"Processing text in streaming mode with {len(chunks)} chunks")

    result = process_chunks_to_hls(
        chunks,
        output_dir=args.output_dir,
        segment_duration=args.segment_duration,
        language=args.language,
    )

    logger.info(f"HLS playlist created at {result['playlist_path']}")
    logger.info(f"Created {result['segment_count']} segments")
    logger.info(f"HLS directory: {result['hls_dir']}")
    logger.info(f"MP3 file created at {result['mp3_file']}")


if __name__ == "__main__":
    main()
