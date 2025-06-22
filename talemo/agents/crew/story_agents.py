"""
Story-related agents for CrewAI integration.
"""
from .base import BaseAgent
from crewai import Task
import logging

logger = logging.getLogger(__name__)

class StorytellerAgent(BaseAgent):
    """
    Agent responsible for creating and developing stories.
    """
    def __init__(self, verbose=True):
        super().__init__(
            name="Storyteller",
            role="Creative Writer and Storyteller",
            goal="Create engaging and age-appropriate stories for children",
            backstory=(
                "You are a master storyteller with years of experience creating "
                "captivating stories for children. You understand narrative structure, "
                "character development, and how to create content that is both "
                "entertaining and educational. You specialize in creating stories "
                "that are appropriate for different age groups and that contain "
                "positive messages and lessons."
            ),
            verbose=verbose
        )
    
    def create_story_task(self, prompt, age_range="4-8"):
        """
        Create a task for generating a story.
        
        Args:
            prompt (str): The story prompt or theme
            age_range (str, optional): The target age range for the story
            
        Returns:
            Task: A CrewAI task for story generation
        """
        return Task(
            description=(
                f"Create a short story based on the prompt: '{prompt}'. "
                f"The story should be appropriate for children aged {age_range}. "
                "Include a title, characters, setting, plot, and a positive message or lesson. "
                "The story should be engaging, imaginative, and approximately 500-800 words long."
            ),
            expected_output=(
                "A complete short story with title, characters, plot, and a clear message. "
                "The story should be well-structured with a beginning, middle, and end."
            ),
            agent=self.agent
        )


class IllustratorAgent(BaseAgent):
    """
    Agent responsible for creating visual descriptions for stories.
    """
    def __init__(self, verbose=True):
        super().__init__(
            name="Illustrator",
            role="Visual Artist and Illustrator",
            goal="Create vivid and engaging visual descriptions for story illustrations",
            backstory=(
                "You are a talented illustrator with a keen eye for visual storytelling. "
                "You excel at translating narrative elements into compelling visual scenes "
                "that capture the imagination of children. Your illustrations are colorful, "
                "expressive, and help bring stories to life."
            ),
            verbose=verbose
        )
    
    def create_illustration_task(self, story):
        """
        Create a task for generating illustration descriptions.
        
        Args:
            story (str): The story text to illustrate
            
        Returns:
            Task: A CrewAI task for illustration description
        """
        return Task(
            description=(
                "Create detailed descriptions for 3-5 key illustrations that would accompany "
                f"the following story: '{story}'. For each illustration, describe the scene, "
                "characters, colors, mood, and composition. These descriptions will be used "
                "to generate actual illustrations."
            ),
            expected_output=(
                "3-5 detailed illustration descriptions, each with a scene number, title, "
                "and comprehensive visual description including characters, setting, colors, "
                "and composition."
            ),
            agent=self.agent
        )


class NarratorAgent(BaseAgent):
    """
    Agent responsible for creating narration scripts and voice guidance.
    """
    def __init__(self, verbose=True):
        super().__init__(
            name="Narrator",
            role="Voice Actor and Narrator",
            goal="Create engaging narration scripts with voice direction",
            backstory=(
                "You are an experienced voice actor and narrator who specializes in "
                "children's content. You understand how to use tone, pacing, and emotion "
                "to bring stories to life through audio. You excel at creating scripts "
                "that guide narrators on how to perform the story for maximum engagement."
            ),
            verbose=verbose
        )
    
    def create_narration_task(self, story):
        """
        Create a task for generating narration scripts.
        
        Args:
            story (str): The story text to narrate
            
        Returns:
            Task: A CrewAI task for narration script generation
        """
        return Task(
            description=(
                f"Create a narration script for the following story: '{story}'. "
                "Break down the story into segments with voice direction notes "
                "indicating tone, emotion, pacing, and any special voice effects. "
                "Include guidance for different character voices if applicable."
            ),
            expected_output=(
                "A complete narration script with the story text broken into segments, "
                "each with clear voice direction notes. Include an introduction and "
                "conclusion with appropriate pacing and tone guidance."
            ),
            agent=self.agent
        )