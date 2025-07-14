# Story Generation

This document describes the story generation functionality in Talemo, including how to use the `generate_story_chapter` function to generate content for story chapters.

## Overview

Talemo provides a service for generating story chapters based on provided metadata. The `generate_story_chapter` function takes a JSON input with story and chapter details, validates the input, generates content for the specified chapter, and returns the completed chapter.

The story generation is implemented as a Celery task, allowing it to run asynchronously in the background. This is particularly useful for longer story generation tasks that might take some time to complete.

## JSON Format

The JSON input for the `generate_story_chapter` function should follow this format:

```json
{
  "story": {
    "title": "{{story_title}}",
    "description": "{{story_description}}",
    "age_group": "{{age_group}}",
    "topic": "{{topic}}",
    "hero": "{{hero}}",
    "chapters": [
      {
        "title": "{{chapter_title}}",
        "place": "{{location}}",
        "tool": "{{tool_used}}",
        "order": {{chapter_number}},
        "content": "{{chapter_content}}"
      },
      {
        "title": "{{new_chapter_title}}",
        "place": "{{new_location}}",
        "tool": "{{new_tool}}",
        "order": {{new_chapter_number}}
      }
    ]
  }
}
```

### Example

Here's an example with sample data:

```json
{
  "story": {
    "title": "The Magic Paintbrush",
    "description": "A tale about creativity and believing in oneself",
    "age_group": "6-8 years",
    "topic": "Art and Imagination",
    "hero": "Lucy",
    "chapters": [
      {
        "title": "The Discovery",
        "place": "Grandmother's Attic",
        "tool": "Paintbrush",
        "order": 1,
        "content": "Lucy was exploring her grandmother's attic when she found an old wooden chest..."
      },
      {
        "title": "The First Painting",
        "place": "Lucy's Room",
        "tool": "Magic Paintbrush",
        "order": 2
      }
    ]
  }
}
```

In this example:
- The first chapter already has content
- The second chapter needs content to be generated

## Using the Function

You can use the `generate_story_chapter` function in your Python code in two ways: asynchronously (default) or synchronously.

### Asynchronous Mode (Default)

In asynchronous mode, the function returns a Celery `AsyncResult` object that you can use to check the status and get the result:

```python
from talemo.stories.services import generate_story_chapter

# Prepare your JSON input
json_input = {
  "story": {
    "title": "The Magic Paintbrush",
    "description": "A tale about creativity and believing in oneself",
    "age_group": "6-8 years",
    "topic": "Art and Imagination",
    "hero": "Lucy",
    "chapters": [
      {
        "title": "The Discovery",
        "place": "Grandmother's Attic",
        "tool": "Paintbrush",
        "order": 1,
        "content": "Lucy was exploring her grandmother's attic when she found an old wooden chest..."
      },
      {
        "place": "Lucy's Room",
        "tool": "Magic Paintbrush",
        "order": 2
      }
    ]
  }
}

# Call the function asynchronously (default)
task_result = generate_story_chapter(json_input)

# Check the task status
print(f"Task ID: {task_result.id}")
print(f"Task status: {task_result.status}")

# Wait for the task to complete and get the result
result = task_result.get()  # This will block until the task completes

# The result will be a dictionary with the completed chapter
print(result)
```

### Synchronous Mode

If you prefer to run the function synchronously (blocking until completion), you can set the `async_mode` parameter to `False`:

```python
from talemo.stories.services import generate_story_chapter

# Prepare your JSON input (same as above)
json_input = {...}

# Call the function synchronously
result = generate_story_chapter(json_input, async_mode=False)

# The result will be a dictionary with the completed chapter
print(result)
```

### Result Structure

In both cases, the result will be a dictionary with the following structure:

```python
{
  "title": "The First Painting",
  "place": "Lucy's Room",
  "tool": "Magic Paintbrush",
  "order": 2,
  "content": "Generated content for the chapter..."
}
```

## Function Behavior

### Service Function

The `generate_story_chapter` function in `services.py`:

1. Provides both synchronous and asynchronous interfaces
2. By default, runs asynchronously as a Celery task
3. Can be run synchronously by setting `async_mode=False`
4. Returns either a Celery `AsyncResult` (async mode) or the completed chapter (sync mode)

### Celery Task

The actual story generation logic is implemented as a Celery task in `tasks.py`:

1. Validates the input structure and required fields
2. Finds or creates the story in the database
3. Identifies the chapter that needs content generation (the one without content)
4. Checks if the chapter already exists in the database
5. Generates content for the chapter
6. Creates or updates the chapter in the database
7. Returns the completed chapter with all fields including the generated content

### Task Monitoring

You can monitor the status of Celery tasks using the Flower dashboard at http://localhost:5555.

## Error Handling

The function will raise a `ValueError` in the following cases:

- Invalid JSON input
- Missing required fields in the story or chapter
- All chapters already have content
- No chapter to generate (empty chapters list)

Make sure to handle these exceptions in your code.

## Integration with LLM

In a production environment, the function would call an LLM API to generate the chapter content. The current implementation uses a placeholder content generator, which should be replaced with an actual LLM integration.
