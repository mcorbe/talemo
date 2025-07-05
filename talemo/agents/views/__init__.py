"""
Import views from the agents app.
"""
# Import the view functions directly from the views_absolute.py file
# which uses absolute imports to avoid circular imports
from .views_absolute import (
    generate_story_api,
    enhance_story_api,
    task_status,
    playground
)

# Re-export the view functions to maintain the expected API
__all__ = ['generate_story_api', 'enhance_story_api', 'task_status', 'playground']
