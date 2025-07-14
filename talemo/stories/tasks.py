"""
Celery tasks for the stories app.
"""
import json
from celery import shared_task
from .models.story import Story
from .models.chapter import Chapter

@shared_task
def generate_story_chapter(json_input):
    """
    Generate a chapter for a story based on the provided JSON input.

    This is a Celery task that can be executed asynchronously.

    The JSON input should follow this format:
    {
      "story": {
        "title": "Story Title",
        "description": "Story Description",
        "age_group": "Age Group",
        "topic": "Topic",
        "hero": "Hero Name",
        "chapters": [
          {
            "title": "Chapter Title",
            "place": "Location",
            "tool": "Tool Used",
            "order": 1,
            "content": "Chapter Content"
          },
          {
            "title": "New Chapter Title",
            "place": "New Location",
            "tool": "New Tool",
            "order": 2
          }
        ]
      }
    }

    The function will:
    1. Validate the input
    2. Find or create the story
    3. Process existing chapters
    4. Generate content for the new chapter
    5. Return the completed chapter

    Args:
        json_input (str or dict): JSON string or dictionary with story and chapter data

    Returns:
        dict: The completed chapter with all fields including generated content
    """
    # Parse JSON if it's a string
    if isinstance(json_input, str):
        try:
            data = json.loads(json_input)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON input")
    else:
        data = json_input

    # Validate input structure
    if not isinstance(data, dict) or 'story' not in data:
        raise ValueError("Input must contain a 'story' object")

    story_data = data['story']
    required_story_fields = ['title', 'description', 'age_group', 'topic', 'hero', 'chapters']
    for field in required_story_fields:
        if field not in story_data:
            raise ValueError(f"Story is missing required field: {field}")

    if not isinstance(story_data['chapters'], list) or len(story_data['chapters']) == 0:
        raise ValueError("Story must contain at least one chapter")

    # Find or create the story
    story, created = Story.objects.get_or_create(
        title=story_data['title'],
        defaults={
            'description': story_data['description'],
            'age_group': story_data['age_group'],
            'topic': story_data['topic'],
            'hero': story_data['hero']
        }
    )

    # If the story exists but wasn't created just now, update its fields
    if not created:
        story.description = story_data['description']
        story.age_group = story_data['age_group']
        story.topic = story_data['topic']
        story.hero = story_data['hero']
        story.save()

    # Process existing chapters
    chapters = story_data['chapters']
    chapter_to_generate = None

    # Find the chapter that needs content generation (the one without content)
    for chapter_data in chapters:
        if 'content' not in chapter_data or not chapter_data['content']:
            chapter_to_generate = chapter_data
            break

    if not chapter_to_generate:
        raise ValueError("All chapters already have content")

    # Validate the chapter to generate
    required_chapter_fields = ['title', 'place', 'tool', 'order']
    for field in required_chapter_fields:
        if field not in chapter_to_generate:
            raise ValueError(f"Chapter to generate is missing required field: {field}")

    # Check if this chapter already exists
    try:
        existing_chapter = Chapter.objects.get(
            story=story,
            order=chapter_to_generate['order']
        )
        # If it exists and has content, return it
        if existing_chapter.content:
            return {
                'title': existing_chapter.title,
                'place': existing_chapter.place,
                'tool': existing_chapter.tool,
                'order': existing_chapter.order,
                'content': existing_chapter.content,
                'story_id': str(story.id)
            }
    except Chapter.DoesNotExist:
        existing_chapter = None

    # Generate content for the chapter
    # In a real implementation, this would call an LLM API
    # For now, we'll create a placeholder content
    generated_content = (
        f"In this chapter, {story.hero} finds themselves in {chapter_to_generate['place']}. "
        f"Using {chapter_to_generate['tool']}, they embark on an adventure related to {story.topic}. "
        f"This story is suitable for children in the {story.age_group} age group."
    )

    # Create or update the chapter
    if existing_chapter:
        existing_chapter.title = chapter_to_generate['title']
        existing_chapter.place = chapter_to_generate['place']
        existing_chapter.tool = chapter_to_generate['tool']
        existing_chapter.content = generated_content
        existing_chapter.save()
        chapter = existing_chapter
    else:
        chapter = Chapter.objects.create(
            story=story,
            title=chapter_to_generate['title'],
            place=chapter_to_generate['place'],
            tool=chapter_to_generate['tool'],
            order=chapter_to_generate['order'],
            content=generated_content
        )

    # Return the completed chapter with story ID
    return {
        'title': chapter.title,
        'place': chapter.place,
        'tool': chapter.tool,
        'order': chapter.order,
        'content': chapter.content,
        'story_id': str(story.id)
    }
