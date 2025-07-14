"""
Services for the stories app.
"""
import json
from .tasks import generate_story_chapter as generate_story_chapter_task

def generate_story_chapter(json_input, async_mode=True):
    """
    Generate a chapter for a story based on the provided JSON input.

    This function provides both synchronous and asynchronous interfaces to the
    story chapter generation functionality. By default, it runs asynchronously
    as a Celery task.

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
        async_mode (bool): If True, runs as a Celery task; if False, runs synchronously

    Returns:
        If async_mode is True:
            AsyncResult: Celery task result that can be used to check status and get the result
        If async_mode is False:
            dict: The completed chapter with all fields including generated content
    """
    if async_mode:
        # Run as a Celery task
        return generate_story_chapter_task.delay(json_input)
    else:
        # Run synchronously
        return generate_story_chapter_task(json_input)
