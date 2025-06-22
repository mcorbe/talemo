"""
Story creation crew for CrewAI integration.
"""
from django.conf import settings
from .base import BaseCrew, langfuse_client
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

    def create_story(self, prompt, age_range="4-8", user_id=None, tenant_id=None):
        """
        Create a complete story with illustrations and narration.

        Args:
            prompt (str): The story prompt or theme
            age_range (str, optional): The target age range for the story
            user_id (str, optional): The ID of the user creating the story
            tenant_id (str, optional): The ID of the tenant

        Returns:
            dict: A dictionary containing the story, illustration descriptions, and narration script
        """
        # Initialize Langfuse trace if enabled
        trace = None
        if settings.LANGTRACE_ENABLED and langfuse_client:
            try:
                trace = langfuse_client.trace(
                    name="story_creation",
                    user_id=user_id,
                    metadata={
                        "prompt": prompt,
                        "age_range": age_range,
                        "tenant_id": tenant_id
                    }
                )
                logger.info(f"Created Langfuse trace for story creation: {prompt[:50]}...")
            except Exception as e:
                logger.error(f"Failed to create Langfuse trace: {e}")
                trace = None

        # Create the story task
        story_task = self.storyteller.create_story_task(prompt, age_range)

        # Add the task to the crew
        self.add_task(story_task)

        # Run the crew to generate the story
        if trace:
            with trace.span(name="generate_story"):
                story = self.run()
                trace.generation(
                    name="story_generation",
                    model="gpt-4",  # This should ideally be dynamic based on the actual model used
                    prompt=prompt,
                    completion=story[:500] + "..." if len(story) > 500 else story,
                )
        else:
            story = self.run()

        # Create the illustration task
        illustration_task = self.illustrator.create_illustration_task(story)

        # Reset the crew and add the illustration task
        self._crew = None
        self.tasks = [illustration_task]

        # Run the crew to generate the illustration descriptions
        if trace:
            with trace.span(name="generate_illustrations"):
                illustration_descriptions = self.run()
                trace.generation(
                    name="illustration_generation",
                    model="gpt-4",  # This should ideally be dynamic based on the actual model used
                    prompt=story[:200] + "...",
                    completion=illustration_descriptions[:500] + "..." if len(illustration_descriptions) > 500 else illustration_descriptions,
                )
        else:
            illustration_descriptions = self.run()

        # Create the narration task
        narration_task = self.narrator.create_narration_task(story)

        # Reset the crew and add the narration task
        self._crew = None
        self.tasks = [narration_task]

        # Run the crew to generate the narration script
        if trace:
            with trace.span(name="generate_narration"):
                narration_script = self.run()
                trace.generation(
                    name="narration_generation",
                    model="gpt-4",  # This should ideally be dynamic based on the actual model used
                    prompt=story[:200] + "...",
                    completion=narration_script[:500] + "..." if len(narration_script) > 500 else narration_script,
                )
        else:
            narration_script = self.run()

        # Log the final result if tracing is enabled
        if trace:
            trace.update(
                output={
                    "story_length": len(story),
                    "illustration_descriptions_length": len(illustration_descriptions),
                    "narration_script_length": len(narration_script)
                }
            )

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

    def enhance_story(self, story, user_id=None, tenant_id=None):
        """
        Enhance an existing story with illustrations and narration.

        Args:
            story (str): The existing story text
            user_id (str, optional): The ID of the user enhancing the story
            tenant_id (str, optional): The ID of the tenant

        Returns:
            dict: A dictionary containing the illustration descriptions and narration script
        """
        # Initialize Langfuse trace if enabled
        trace = None
        if settings.LANGTRACE_ENABLED and langfuse_client:
            try:
                trace = langfuse_client.trace(
                    name="story_enhancement",
                    user_id=user_id,
                    metadata={
                        "story_length": len(story),
                        "tenant_id": tenant_id
                    }
                )
                logger.info(f"Created Langfuse trace for story enhancement: {story[:50]}...")
            except Exception as e:
                logger.error(f"Failed to create Langfuse trace: {e}")
                trace = None

        # Create the illustration task
        illustration_task = self.illustrator.create_illustration_task(story)

        # Add the task to the crew
        self.add_task(illustration_task)

        # Run the crew to generate the illustration descriptions
        if trace:
            with trace.span(name="generate_illustrations"):
                illustration_descriptions = self.run()
                trace.generation(
                    name="illustration_generation",
                    model="gpt-4",  # This should ideally be dynamic based on the actual model used
                    prompt=story[:200] + "...",
                    completion=illustration_descriptions[:500] + "..." if len(illustration_descriptions) > 500 else illustration_descriptions,
                )
        else:
            illustration_descriptions = self.run()

        # Create the narration task
        narration_task = self.narrator.create_narration_task(story)

        # Reset the crew and add the narration task
        self._crew = None
        self.tasks = [narration_task]

        # Run the crew to generate the narration script
        if trace:
            with trace.span(name="generate_narration"):
                narration_script = self.run()
                trace.generation(
                    name="narration_generation",
                    model="gpt-4",  # This should ideally be dynamic based on the actual model used
                    prompt=story[:200] + "...",
                    completion=narration_script[:500] + "..." if len(narration_script) > 500 else narration_script,
                )
        else:
            narration_script = self.run()

        # Log the final result if tracing is enabled
        if trace:
            trace.update(
                output={
                    "illustration_descriptions_length": len(illustration_descriptions),
                    "narration_script_length": len(narration_script)
                }
            )

        # Return the results
        return {
            "illustration_descriptions": illustration_descriptions,
            "narration_script": narration_script
        }
