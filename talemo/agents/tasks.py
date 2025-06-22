"""
Celery tasks for the agents app.
"""
from celery import shared_task
from talemo.agents.crew import StoryCreationCrew, StoryEnhancementCrew
import logging

logger = logging.getLogger(__name__)

@shared_task
def generate_story(prompt, age_range="4-8"):
    """
    Generate a complete story with illustrations and narration.
    
    Args:
        prompt (str): The story prompt or theme
        age_range (str, optional): The target age range for the story
        
    Returns:
        dict: A dictionary containing the story, illustration descriptions, and narration script
    """
    logger.info(f"Generating story with prompt: {prompt}, age range: {age_range}")
    
    try:
        # Create the story creation crew
        crew = StoryCreationCrew(verbose=True)
        
        # Generate the story
        result = crew.create_story(prompt, age_range)
        
        logger.info("Story generation completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error generating story: {str(e)}")
        raise

@shared_task
def enhance_story(story):
    """
    Enhance an existing story with illustrations and narration.
    
    Args:
        story (str): The existing story text
        
    Returns:
        dict: A dictionary containing the illustration descriptions and narration script
    """
    logger.info(f"Enhancing story: {story[:100]}...")
    
    try:
        # Create the story enhancement crew
        crew = StoryEnhancementCrew(verbose=True)
        
        # Enhance the story
        result = crew.enhance_story(story)
        
        logger.info("Story enhancement completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error enhancing story: {str(e)}")
        raise