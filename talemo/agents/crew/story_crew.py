"""
Story creation crew for CrewAI integration.
"""
from .base import BaseCrew
from .story_agents import StorytellerAgent, IllustratorAgent, NarratorAgent
import logging

logger = logging.getLogger(__name__)

class StoryCreationCrew(BaseCrew):
    """
    A crew for creating complete stories with illustrations and narration.
    """
    def __init__(self, verbose=True):
        """
        Initialize the story creation crew.
        
        Args:
            verbose (bool, optional): Whether to enable verbose logging
        """
        # Create the agents
        self.storyteller = StorytellerAgent(verbose=verbose)
        self.illustrator = IllustratorAgent(verbose=verbose)
        self.narrator = NarratorAgent(verbose=verbose)
        
        # Initialize the base crew with the agents
        super().__init__(
            agents=[self.storyteller, self.illustrator, self.narrator],
            verbose=verbose
        )
    
    def create_story(self, prompt, age_range="4-8"):
        """
        Create a complete story with illustrations and narration.
        
        Args:
            prompt (str): The story prompt or theme
            age_range (str, optional): The target age range for the story
            
        Returns:
            dict: A dictionary containing the story, illustration descriptions, and narration script
        """
        # Create the story task
        story_task = self.storyteller.create_story_task(prompt, age_range)
        
        # Add the task to the crew
        self.add_task(story_task)
        
        # Run the crew to generate the story
        story = self.run()
        
        # Create the illustration task
        illustration_task = self.illustrator.create_illustration_task(story)
        
        # Reset the crew and add the illustration task
        self._crew = None
        self.tasks = [illustration_task]
        
        # Run the crew to generate the illustration descriptions
        illustration_descriptions = self.run()
        
        # Create the narration task
        narration_task = self.narrator.create_narration_task(story)
        
        # Reset the crew and add the narration task
        self._crew = None
        self.tasks = [narration_task]
        
        # Run the crew to generate the narration script
        narration_script = self.run()
        
        # Return the results
        return {
            "story": story,
            "illustration_descriptions": illustration_descriptions,
            "narration_script": narration_script
        }


class StoryEnhancementCrew(BaseCrew):
    """
    A crew for enhancing existing stories with illustrations and narration.
    """
    def __init__(self, verbose=True):
        """
        Initialize the story enhancement crew.
        
        Args:
            verbose (bool, optional): Whether to enable verbose logging
        """
        # Create the agents
        self.illustrator = IllustratorAgent(verbose=verbose)
        self.narrator = NarratorAgent(verbose=verbose)
        
        # Initialize the base crew with the agents
        super().__init__(
            agents=[self.illustrator, self.narrator],
            verbose=verbose
        )
    
    def enhance_story(self, story):
        """
        Enhance an existing story with illustrations and narration.
        
        Args:
            story (str): The existing story text
            
        Returns:
            dict: A dictionary containing the illustration descriptions and narration script
        """
        # Create the illustration task
        illustration_task = self.illustrator.create_illustration_task(story)
        
        # Add the task to the crew
        self.add_task(illustration_task)
        
        # Run the crew to generate the illustration descriptions
        illustration_descriptions = self.run()
        
        # Create the narration task
        narration_task = self.narrator.create_narration_task(story)
        
        # Reset the crew and add the narration task
        self._crew = None
        self.tasks = [narration_task]
        
        # Run the crew to generate the narration script
        narration_script = self.run()
        
        # Return the results
        return {
            "illustration_descriptions": illustration_descriptions,
            "narration_script": narration_script
        }