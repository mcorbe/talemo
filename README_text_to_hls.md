# Text to HLS Audio Converter

A simple Python script that converts text to HLS audio using Google Text-to-Speech (gTTS) for text-to-speech and ffmpeg for HLS playlist creation.

## Features

- Converts text to speech using Google Text-to-Speech (gTTS)
- Processes text into audio with natural-sounding speech
- Creates HLS playlist with configurable segment duration
- Generates a final MP3 audio file
- Supports multiple languages
- Handles cleanup of temporary files
- Supports streaming mode for processing text in chunks incrementally

## Requirements

- Python 3.6+
- ffmpeg
- Required Python packages:
  - gtts
  - nltk

## Installation

1. Make sure ffmpeg is installed on your system:
   ```
   # Ubuntu/Debian
   sudo apt-get install ffmpeg

   # macOS
   brew install ffmpeg

   # Windows
   # Download from https://ffmpeg.org/download.html
   ```

2. Install the required Python packages:
   ```
   pip install gtts nltk
   ```

## Usage

### Basic Usage

```bash
python text_to_hls.py
```

This will use the default text (the story about Freddy the fox) and create HLS files in a temporary directory.

### Custom Text

```bash
python text_to_hls.py --text-file your_text_file.txt
```

### Custom Output Directory

```bash
python text_to_hls.py --output-dir /path/to/output
```

### Streaming Mode

```bash
python text_to_hls.py --streaming --chunk-size 100
```

This will process the text in chunks of 100 words each, creating HLS segments incrementally as each chunk is processed. This is useful for:
- Processing very long texts
- Generating audio in real-time as text is being generated
- Reducing memory usage for large texts

### All Options

```bash
python text_to_hls.py --help
```

Output:
```
usage: text_to_hls.py [-h] [--output-dir OUTPUT_DIR] [--segment-duration SEGMENT_DURATION] [--language LANGUAGE] [--speaker-embedding SPEAKER_EMBEDDING] [--text-file TEXT_FILE] [--streaming] [--chunk-size CHUNK_SIZE]

Convert text to HLS audio using Google Text-to-Speech

options:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
                        Output directory
  --segment-duration SEGMENT_DURATION, -d SEGMENT_DURATION
                        Segment duration in seconds
  --language LANGUAGE, -l LANGUAGE
                        Language code (e.g., en, fr, es)
  --speaker-embedding SPEAKER_EMBEDDING, -s SPEAKER_EMBEDDING
                        Path to speaker embedding file (not used with gTTS)
  --text-file TEXT_FILE, -t TEXT_FILE
                        Path to text file
  --streaming           Use streaming mode to process text in chunks
  --chunk-size CHUNK_SIZE
                        Number of words per chunk in streaming mode (default: 200)
```

## Examples

### Standard Mode

```bash
python text_to_hls.py --output-dir ./output --segment-duration 3 --language en
```

This will:
1. Use the default text (the story about Freddy the fox)
2. Create HLS files in the `./output` directory
3. Use 3-second segments
4. Use English as the language

### Streaming Mode

```bash
python text_to_hls.py --output-dir ./output --segment-duration 2 --language fr --streaming --chunk-size 150
```

This will:
1. Use the default text (the story about Freddy the fox)
2. Process the text in chunks of 150 words each
3. Create HLS segments incrementally as each chunk is processed
4. Use 2-second segments
5. Use French as the language
6. Store all files in the `./output` directory

## Output

The script creates:
- PCM audio files for the text
- HLS playlist and segment files
- A final MP3 audio file

The output structure:
```
output/
├── pcm/
│   └── audio.pcm
├── hls/
│   ├── playlist.m3u8
│   ├── segment_000.ts
│   ├── segment_001.ts
│   └── ...
└── mp3/
    └── audio.mp3
```

## Notes

- The script requires an internet connection as it uses Google's Text-to-Speech service.
- For very long texts, the script will make multiple API calls to Google's service.
- Processing long texts may take significant time depending on your internet connection.
- By default, temporary directories are not cleaned up to allow inspection of the generated files.
- The language parameter accepts standard language codes (e.g., 'en' for English, 'fr' for French, 'es' for Spanish).

## Recent Changes

- Changed output format from MP4 to MP3 for better compatibility and smaller file sizes
- Fixed an issue with PCM file concatenation in streaming mode
- Improved error handling for ffmpeg operations
- Added fallback mechanisms to ensure audio files are always created, even if audio processing fails
- Added streaming mode to process text in chunks incrementally
- Implemented a new class `StreamingTextToHLS` for handling incremental processing
- Added command-line arguments `--streaming` and `--chunk-size` to control streaming behavior
- Fixed an issue where the script was producing silent audio
- Successfully implemented audio generation using Google Text-to-Speech (gTTS)
- Ensured proper creation of both HLS playlists and audio files
