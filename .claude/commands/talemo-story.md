# Talemo Story Management

Create and manage AI-powered stories with chapters, audio generation, and illustrations.

## Purpose

This command helps you work with Talemo's story generation system, including CrewAI agents, text-to-speech, and HLS streaming.

## Usage

```
/talemo-story
```

## What this command does

1. **Creates story models** with proper structure
2. **Generates stories** using CrewAI agents
3. **Converts text to speech** using gTTS
4. **Sets up HLS streaming** for audio delivery
5. **Manages story chapters** and metadata

## Example Story Model

```python
# talemo/stories/models/story.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid

User = get_user_model()

class Story(models.Model):
    """AI-generated story with audio narration."""
    
    GENRE_CHOICES = [
        ('adventure', 'Adventure'),
        ('fantasy', 'Fantasy'),
        ('mystery', 'Mystery'),
        ('scifi', 'Science Fiction'),
        ('educational', 'Educational'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('generating', 'Generating'),
        ('ready', 'Ready'),
        ('published', 'Published'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    target_age = models.IntegerField(help_text="Target age for the story")
    
    # AI Generation
    prompt = models.TextField(help_text="Initial prompt for story generation")
    ai_model = models.CharField(max_length=50, default='gpt-4')
    generation_params = models.JSONField(default=dict, blank=True)
    
    # Content
    synopsis = models.TextField(blank=True)
    moral_lesson = models.TextField(blank=True)
    
    # Media
    cover_image = models.ImageField(upload_to='stories/covers/', null=True, blank=True)
    audio_url = models.URLField(blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    
    # Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Stats
    play_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
```

## Story Generation with CrewAI

```python
# talemo/stories/ai_crew.py
from crewai import Agent, Task, Crew
from langchain.llms import OpenAI

class StoryGenerationCrew:
    """CrewAI crew for generating children's stories."""
    
    def __init__(self, llm=None):
        self.llm = llm or OpenAI(temperature=0.7)
    
    def create_agents(self):
        # Story Writer Agent
        self.writer = Agent(
            role='Children Story Writer',
            goal='Create engaging and educational stories for children',
            backstory='You are an experienced children\'s book author...',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Story Editor Agent
        self.editor = Agent(
            role='Story Editor',
            goal='Ensure stories are age-appropriate and engaging',
            backstory='You are a professional editor specializing in children\'s literature...',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Narrator Agent
        self.narrator = Agent(
            role='Audio Narrator',
            goal='Adapt stories for audio narration',
            backstory='You are a professional audiobook narrator...',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_story(self, prompt, genre, target_age):
        """Generate a complete story with chapters."""
        
        # Create tasks
        writing_task = Task(
            description=f"Write a {genre} story for {target_age} year olds based on: {prompt}",
            agent=self.writer,
            expected_output="A complete story with title, chapters, and moral lesson"
        )
        
        editing_task = Task(
            description="Edit the story for age-appropriateness and engagement",
            agent=self.editor,
            expected_output="An edited, polished story"
        )
        
        narration_task = Task(
            description="Adapt the story for audio narration with proper pacing",
            agent=self.narrator,
            expected_output="Story text optimized for text-to-speech"
        )
        
        # Create crew
        crew = Crew(
            agents=[self.writer, self.editor, self.narrator],
            tasks=[writing_task, editing_task, narration_task],
            verbose=True
        )
        
        # Execute crew
        result = crew.kickoff()
        return result
```

## Audio Generation Task

```python
# talemo/stories/tasks.py
from celery import shared_task
from talemo.audiostream.tts import TextToSpeech
from talemo.audiostream.hls import HLSGenerator
import logging

logger = logging.getLogger(__name__)

@shared_task
def generate_story_audio(story_id):
    """Generate audio for a story and create HLS stream."""
    from .models import Story
    
    try:
        story = Story.objects.get(id=story_id)
        
        # Initialize TTS
        tts = TextToSpeech()
        
        # Generate audio for each chapter
        audio_files = []
        for chapter in story.chapters.all():
            audio_path = tts.generate_speech(
                text=chapter.content,
                output_path=f"media/stories/{story_id}/chapter_{chapter.order}.mp3"
            )
            audio_files.append(audio_path)
            chapter.audio_url = audio_path
            chapter.save()
        
        # Create HLS stream
        hls = HLSGenerator()
        hls_url = hls.create_stream(
            audio_files=audio_files,
            output_dir=f"media/hls/{story_id}/"
        )
        
        # Update story
        story.audio_url = hls_url
        story.status = 'ready'
        story.save()
        
        logger.info(f"Audio generation completed for story {story_id}")
        return hls_url
        
    except Exception as e:
        logger.error(f"Audio generation failed for story {story_id}: {str(e)}")
        story.status = 'failed'
        story.save()
        raise
```

## Story Service

```python
# talemo/stories/services.py
from .ai_crew import StoryGenerationCrew
from .models import Story, Chapter
from .tasks import generate_story_audio

class StoryService:
    """Service layer for story operations."""
    
    @staticmethod
    def create_story(user, prompt, genre, target_age):
        """Create a new AI-generated story."""
        
        # Create story instance
        story = Story.objects.create(
            author=user,
            prompt=prompt,
            genre=genre,
            target_age=target_age,
            status='generating'
        )
        
        # Generate story content
        crew = StoryGenerationCrew()
        story_content = crew.create_story(prompt, genre, target_age)
        
        # Parse and save story content
        story.title = story_content.get('title')
        story.description = story_content.get('description')
        story.synopsis = story_content.get('synopsis')
        story.moral_lesson = story_content.get('moral_lesson')
        story.save()
        
        # Create chapters
        for idx, chapter_data in enumerate(story_content.get('chapters', [])):
            Chapter.objects.create(
                story=story,
                title=chapter_data.get('title'),
                content=chapter_data.get('content'),
                order=idx + 1
            )
        
        # Queue audio generation
        generate_story_audio.delay(str(story.id))
        
        return story
```

## Usage in Views

```python
# talemo/stories/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Story
from .services import StoryService
from .serializers import StorySerializer

class StoryViewSet(viewsets.ModelViewSet):
    """API endpoint for story management."""
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate a new story based on prompt."""
        prompt = request.data.get('prompt')
        genre = request.data.get('genre', 'adventure')
        target_age = request.data.get('target_age', 8)
        
        story = StoryService.create_story(
            user=request.user,
            prompt=prompt,
            genre=genre,
            target_age=target_age
        )
        
        serializer = self.get_serializer(story)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def stream(self, request, pk=None):
        """Get HLS streaming URL for story."""
        story = self.get_object()
        if story.audio_url:
            return Response({
                'stream_url': story.audio_url,
                'duration': story.duration_seconds
            })
        return Response(
            {'error': 'Audio not ready yet'}, 
            status=status.HTTP_404_NOT_FOUND
        )
```

## Testing Story Generation

```python
# talemo/stories/tests/test_story_generation.py
import pytest
from django.contrib.auth import get_user_model
from talemo.stories.services import StoryService
from talemo.stories.models import Story

User = get_user_model()

@pytest.mark.django_db
class TestStoryGeneration:
    def test_create_story(self, user):
        """Test story creation with AI generation."""
        story = StoryService.create_story(
            user=user,
            prompt="A brave little mouse saves the day",
            genre="adventure",
            target_age=6
        )
        
        assert story.title is not None
        assert story.status == 'generating'
        assert story.chapters.count() > 0
        
    def test_audio_generation_task(self, story_with_chapters):
        """Test audio generation for story."""
        from talemo.stories.tasks import generate_story_audio
        
        result = generate_story_audio(str(story_with_chapters.id))
        
        story_with_chapters.refresh_from_db()
        assert story_with_chapters.audio_url is not None
        assert story_with_chapters.status == 'ready'
```