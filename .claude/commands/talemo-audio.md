# Talemo Audio Streaming

Configure and manage HLS audio streaming, text-to-speech, and audio processing pipelines.

## Purpose

This command helps you work with Talemo's audio streaming infrastructure, including HLS streaming, TTS conversion, and audio processing.

## Usage

```
/talemo-audio
```

## What this command does

1. **Sets up HLS streaming** for low-latency audio delivery
2. **Configures text-to-speech** with gTTS
3. **Creates audio processing pipelines** with FFmpeg
4. **Manages streaming sessions** and cleanup
5. **Implements audio storage** with MinIO/S3

## HLS Streaming Implementation

```python
# talemo/audiostream/hls.py
import os
import subprocess
import logging
from pathlib import Path
from django.conf import settings
from .storage import AudioStorage

logger = logging.getLogger(__name__)

class HLSStreamGenerator:
    """Generate HLS streams from audio files."""
    
    def __init__(self):
        self.storage = AudioStorage()
        self.segment_duration = 2  # seconds
        self.playlist_type = 'event'  # or 'vod' for static content
    
    def create_stream(self, audio_file, output_dir):
        """Convert audio file to HLS format."""
        try:
            # Ensure output directory exists
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate unique stream ID
            stream_id = self._generate_stream_id()
            
            # FFmpeg command for HLS generation
            ffmpeg_cmd = [
                'ffmpeg',
                '-i', audio_file,
                '-c:a', 'aac',  # Audio codec
                '-b:a', '128k',  # Bitrate
                '-ac', '2',  # Stereo
                '-ar', '44100',  # Sample rate
                '-f', 'hls',  # Output format
                '-hls_time', str(self.segment_duration),
                '-hls_list_size', '0',  # Keep all segments
                '-hls_flags', 'independent_segments',
                '-hls_segment_type', 'mpegts',
                '-hls_segment_filename', f'{output_dir}/segment_%03d.ts',
                '-hls_playlist_type', self.playlist_type,
                '-master_pl_name', 'master.m3u8',
                f'{output_dir}/playlist.m3u8'
            ]
            
            # Execute FFmpeg
            process = subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            
            # Upload to storage
            playlist_url = self._upload_to_storage(output_dir, stream_id)
            
            logger.info(f"HLS stream created: {stream_id}")
            return playlist_url
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr.decode()}")
            raise
        except Exception as e:
            logger.error(f"HLS generation failed: {str(e)}")
            raise
    
    def _generate_stream_id(self):
        """Generate unique stream identifier."""
        import uuid
        return str(uuid.uuid4())
    
    def _upload_to_storage(self, local_dir, stream_id):
        """Upload HLS files to MinIO/S3."""
        remote_path = f"hls/{stream_id}/"
        
        # Upload all .ts and .m3u8 files
        for file_path in Path(local_dir).glob("*"):
            if file_path.suffix in ['.ts', '.m3u8']:
                remote_file = remote_path + file_path.name
                self.storage.upload_file(str(file_path), remote_file)
        
        # Return playlist URL
        return self.storage.get_url(remote_path + "playlist.m3u8")
```

## Text-to-Speech Service

```python
# talemo/audiostream/tts.py
import os
import tempfile
from gtts import gTTS
import logging
from django.conf import settings
from .storage import AudioStorage

logger = logging.getLogger(__name__)

class TextToSpeechService:
    """Convert text to speech using various TTS engines."""
    
    def __init__(self, language='en', tld='com'):
        self.language = language
        self.tld = tld  # Top-level domain for accent
        self.storage = AudioStorage()
    
    def generate_speech(self, text, voice_settings=None):
        """Generate speech audio from text."""
        try:
            # Apply voice settings if provided
            lang = voice_settings.get('language', self.language) if voice_settings else self.language
            slow = voice_settings.get('slow', False) if voice_settings else False
            
            # Create gTTS instance
            tts = gTTS(
                text=text,
                lang=lang,
                slow=slow,
                tld=self.tld
            )
            
            # Generate temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                tts.save(tmp_file.name)
                tmp_path = tmp_file.name
            
            # Upload to storage
            remote_path = f"tts/{self._generate_filename()}.mp3"
            audio_url = self.storage.upload_file(tmp_path, remote_path)
            
            # Cleanup
            os.unlink(tmp_path)
            
            logger.info(f"TTS audio generated: {remote_path}")
            return audio_url
            
        except Exception as e:
            logger.error(f"TTS generation failed: {str(e)}")
            raise
    
    def generate_chapter_audio(self, chapter):
        """Generate audio for a story chapter."""
        # Add narrative markers for better audio
        narrative_text = self._add_narrative_markers(chapter.content)
        
        # Generate with chapter-specific settings
        voice_settings = {
            'language': chapter.story.language,
            'slow': chapter.story.target_age < 6  # Slower for younger kids
        }
        
        return self.generate_speech(narrative_text, voice_settings)
    
    def _add_narrative_markers(self, text):
        """Add pauses and emphasis for better narration."""
        # Add pauses after sentences
        text = text.replace('. ', '. ... ')
        text = text.replace('! ', '! ... ')
        text = text.replace('? ', '? ... ')
        
        # Add emphasis markers (handled by TTS engine)
        return text
    
    def _generate_filename(self):
        """Generate unique filename."""
        import uuid
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{timestamp}_{uuid.uuid4().hex[:8]}"
```

## Audio Processing Pipeline

```python
# talemo/audiostream/pipeline.py
import os
import subprocess
from celery import chain, group
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class AudioPipeline:
    """Process audio through various stages."""
    
    def __init__(self):
        self.temp_dir = settings.MEDIA_ROOT / 'temp'
        self.temp_dir.mkdir(exist_ok=True)
    
    def process_story_audio(self, story):
        """Complete audio processing pipeline for a story."""
        from .tasks import (
            generate_chapter_audio,
            concatenate_audio_files,
            generate_hls_stream,
            cleanup_temp_files
        )
        
        # Create processing chain
        workflow = chain(
            # Generate audio for each chapter in parallel
            group(
                generate_chapter_audio.s(chapter.id)
                for chapter in story.chapters.all()
            ),
            # Concatenate all chapter audio files
            concatenate_audio_files.s(story.id),
            # Generate HLS stream
            generate_hls_stream.s(),
            # Cleanup temporary files
            cleanup_temp_files.s()
        )
        
        # Execute workflow
        result = workflow.apply_async()
        return result.id
    
    def normalize_audio(self, audio_file):
        """Normalize audio levels."""
        output_file = audio_file.replace('.mp3', '_normalized.mp3')
        
        cmd = [
            'ffmpeg',
            '-i', audio_file,
            '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',  # EBU R128 normalization
            '-c:a', 'libmp3lame',
            '-b:a', '128k',
            output_file
        ]
        
        subprocess.run(cmd, check=True)
        return output_file
    
    def add_background_music(self, voice_file, music_file, output_file):
        """Mix voice with background music."""
        cmd = [
            'ffmpeg',
            '-i', voice_file,
            '-i', music_file,
            '-filter_complex',
            '[1:a]volume=0.1[music];[0:a][music]amix=inputs=2:duration=first',
            '-c:a', 'libmp3lame',
            '-b:a', '128k',
            output_file
        ]
        
        subprocess.run(cmd, check=True)
        return output_file
```

## Audio Storage with MinIO

```python
# talemo/audiostream/storage.py
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class AudioStorage:
    """Handle audio file storage in MinIO/S3."""
    
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            use_ssl=settings.AWS_S3_USE_SSL,
            verify=settings.AWS_S3_VERIFY
        )
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist."""
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except ClientError:
            self.client.create_bucket(Bucket=self.bucket)
            logger.info(f"Created bucket: {self.bucket}")
    
    def upload_file(self, local_path, remote_path):
        """Upload file to storage."""
        try:
            self.client.upload_file(
                local_path,
                self.bucket,
                remote_path,
                ExtraArgs={'ContentType': self._get_content_type(remote_path)}
            )
            return self.get_url(remote_path)
        except Exception as e:
            logger.error(f"Upload failed: {str(e)}")
            raise
    
    def get_url(self, remote_path):
        """Get public URL for file."""
        return f"{settings.AWS_S3_ENDPOINT_URL}/{self.bucket}/{remote_path}"
    
    def _get_content_type(self, filename):
        """Determine content type from filename."""
        if filename.endswith('.m3u8'):
            return 'application/vnd.apple.mpegurl'
        elif filename.endswith('.ts'):
            return 'video/mp2t'
        elif filename.endswith('.mp3'):
            return 'audio/mpeg'
        return 'application/octet-stream'
```

## Celery Tasks for Audio Processing

```python
# talemo/audiostream/tasks.py
from celery import shared_task
import os
import logging
from .tts import TextToSpeechService
from .hls import HLSStreamGenerator
from .pipeline import AudioPipeline

logger = logging.getLogger(__name__)

@shared_task
def generate_chapter_audio(chapter_id):
    """Generate audio for a single chapter."""
    from talemo.stories.models import Chapter
    
    chapter = Chapter.objects.get(id=chapter_id)
    tts = TextToSpeechService()
    
    audio_url = tts.generate_chapter_audio(chapter)
    chapter.audio_url = audio_url
    chapter.save()
    
    return {
        'chapter_id': chapter_id,
        'audio_url': audio_url,
        'order': chapter.order
    }

@shared_task
def concatenate_audio_files(chapter_results, story_id):
    """Concatenate chapter audio files into single file."""
    from talemo.stories.models import Story
    
    # Sort chapters by order
    sorted_results = sorted(chapter_results, key=lambda x: x['order'])
    
    # Download audio files locally for processing
    audio_files = []
    for result in sorted_results:
        # Download from storage
        local_file = download_from_storage(result['audio_url'])
        audio_files.append(local_file)
    
    # Create file list for FFmpeg
    list_file = create_concat_list(audio_files)
    
    # Concatenate with FFmpeg
    output_file = f"/tmp/story_{story_id}_complete.mp3"
    concat_cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file,
        '-c', 'copy',
        output_file
    ]
    
    subprocess.run(concat_cmd, check=True)
    
    return {
        'story_id': story_id,
        'audio_file': output_file
    }

@shared_task
def generate_hls_stream(concat_result):
    """Generate HLS stream from concatenated audio."""
    story_id = concat_result['story_id']
    audio_file = concat_result['audio_file']
    
    hls = HLSStreamGenerator()
    output_dir = f"/tmp/hls_{story_id}"
    
    stream_url = hls.create_stream(audio_file, output_dir)
    
    # Update story with stream URL
    from talemo.stories.models import Story
    story = Story.objects.get(id=story_id)
    story.audio_url = stream_url
    story.status = 'ready'
    story.save()
    
    return {
        'story_id': story_id,
        'stream_url': stream_url,
        'temp_files': [audio_file, output_dir]
    }

@shared_task
def cleanup_temp_files(process_result):
    """Clean up temporary files after processing."""
    import shutil
    
    for temp_file in process_result.get('temp_files', []):
        try:
            if os.path.isdir(temp_file):
                shutil.rmtree(temp_file)
            elif os.path.isfile(temp_file):
                os.unlink(temp_file)
        except Exception as e:
            logger.warning(f"Failed to cleanup {temp_file}: {str(e)}")
    
    return process_result
```

## Testing Audio Pipeline

```python
# talemo/audiostream/tests/test_audio_pipeline.py
import pytest
from unittest.mock import patch, MagicMock
from talemo.audiostream.pipeline import AudioPipeline
from talemo.audiostream.tts import TextToSpeechService

@pytest.mark.django_db
class TestAudioPipeline:
    def test_tts_generation(self):
        """Test text-to-speech generation."""
        tts = TextToSpeechService()
        
        with patch('gtts.gTTS.save') as mock_save:
            audio_url = tts.generate_speech("Hello, world!")
            
            assert audio_url is not None
            mock_save.assert_called_once()
    
    def test_hls_stream_generation(self, tmp_path):
        """Test HLS stream generation."""
        from talemo.audiostream.hls import HLSStreamGenerator
        
        # Create test audio file
        test_audio = tmp_path / "test.mp3"
        test_audio.write_text("fake audio data")
        
        hls = HLSStreamGenerator()
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            output_dir = tmp_path / "hls_output"
            stream_url = hls.create_stream(str(test_audio), str(output_dir))
            
            # Verify FFmpeg was called
            assert mock_run.called
            ffmpeg_cmd = mock_run.call_args[0][0]
            assert 'ffmpeg' in ffmpeg_cmd
            assert '-f' in ffmpeg_cmd
            assert 'hls' in ffmpeg_cmd
```