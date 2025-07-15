"""
Celery tasks for the stories app.
"""
import json
import time
from celery import shared_task
from .models.story import Story
from .models.chapter import Chapter
from .ai_crew import create_story_generation_crew

@shared_task
def test_task(x, y):
    """
    A simple test task that adds two numbers.

    This task is used to verify that the Celery worker is processing tasks.
    It includes a small delay to simulate processing time.

    Args:
        x (int): First number
        y (int): Second number

    Returns:
        dict: A dictionary containing the result and a timestamp
    """
    # Simulate processing time
    time.sleep(5)

    # Perform the calculation
    result = x + y

    # Return the result with a timestamp
    return {
        'result': result,
        'timestamp': time.time()
    }

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
    required_story_fields = ['age_group', 'topic', 'hero', 'chapters']
    for field in required_story_fields:
        if field not in story_data:
            raise ValueError(f"Story is missing required field: {field}")

    if not isinstance(story_data['chapters'], list) or len(story_data['chapters']) == 0:
        raise ValueError("Story must contain at least one chapter")

    # Find or create the story
    story, created = Story.objects.get_or_create(
        age_group=story_data['age_group'],
        topic=story_data['topic'],
        hero=story_data['hero'],
    )

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
    required_chapter_fields = ['place', 'tool', 'order']
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
            print(f"Chapter {existing_chapter.title} already exists and has content, returning it...")
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

    # Generate content for the chapter using CrewAI
    # Prepare story data for the crew
    story_data = {
        'title': story.title,
        'description': story.description,
        'age_group': story.age_group,
        'topic': story.topic,
        'hero': story.hero
    }

    # Check if this is the first chapter and if we need to generate a story title
    generate_story_title = False
    if chapter_to_generate['order'] == 1:
        # If the story title is empty or a placeholder, generate a new one
        if not story.title or story.title == "Untitled Story":
            generate_story_title = True

    # Generate the chapter content and title using CrewAI
    print(json.dumps({
        'story_data': story_data,
        'chapter_to_generate': chapter_to_generate,
        'generate_story_title': generate_story_title
    }))
    generated_chapter = create_story_generation_crew(story_data, chapter_to_generate, generate_story_title)

    # Extract the title and content
    generated_title = generated_chapter['title']
    generated_content = generated_chapter['content']

    # Update the story title if a new one was generated
    if generate_story_title and 'story_title' in generated_chapter:
        story.title = generated_chapter['story_title']
        story.save()

    print(f"Generated title: {generated_title}")
    print(f"Generated content: {generated_content}")

    # Create or update the chapter
    if existing_chapter:
        existing_chapter.title = generated_title
        existing_chapter.place = chapter_to_generate['place']
        existing_chapter.tool = chapter_to_generate['tool']
        existing_chapter.content = generated_content
        existing_chapter.save()
        chapter = existing_chapter
    else:
        chapter = Chapter.objects.create(
            story=story,
            title=generated_title,
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
