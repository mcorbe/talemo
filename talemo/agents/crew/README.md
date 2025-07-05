# CrewAI Integration for Talemo

This directory contains the CrewAI integration for the Talemo platform. CrewAI is used to create and manage AI agents that generate and enhance stories for the platform.

## Overview

The CrewAI integration consists of the following components:

1. **Base Classes**: Abstract base classes for agents and crews
2. **Story Agents**: Specific agent implementations for story creation and enhancement
3. **Story Crews**: Crew implementations that coordinate multiple agents

## File Structure

- `base.py`: Contains the `BaseAgent` and `BaseCrew` classes
- `story_agents.py`: Contains the `StorytellerAgent`, `IllustratorAgent`, and `NarratorAgent` classes
- `story_crew.py`: Contains the `StoryCreationCrew` and `StoryEnhancementCrew` classes
- `__init__.py`: Exports all the classes for easy importing

## Usage

### Basic Usage

```python
from talemo.agents.crew import StoryCreationCrew

# Create a story creation crew
crew = StoryCreationCrew(verbose=True)

# Generate a story
result = crew.create_story(
    prompt="A curious cat discovers a magical garden",
    age_range="4-8"
)

# Access the results
story = result["story"]
illustration_descriptions = result["illustration_descriptions"]
narration_script = result["narration_script"]
```

### Using with Celery

The agents are designed to be used with Celery for asynchronous processing. See `talemo/agents/tasks.py` for examples of how to use the agents with Celery.

```python
from talemo.agents import generate_story

# Start a Celery task to generate a story
task = generate_story.delay(
    prompt="A curious cat discovers a magical garden",
    age_range="4-8"
)

# Get the task ID for later retrieval
task_id = task.id
```

## Configuration

The CrewAI integration uses the following settings from `settings.py`:

- `OPENAI_API_KEY`: The API key for OpenAI, used by the agents
- `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY`: Optional keys for AI observability

## Adding New Agents

To add a new agent:

1. Create a new class that inherits from `BaseAgent`
2. Implement the agent's specific functionality
3. Add the agent to a crew or create a new crew for it

Example:

```python
from talemo.agents.crew import BaseAgent


class EditorAgent(BaseAgent):
    """
    Agent responsible for editing and refining stories.
    """

    def __init__(self, verbose=True):
        super().__init__(
            name="Editor",
            role="Story Editor",
            goal="Refine and improve stories for clarity and engagement",
            backstory="You are an experienced editor with a keen eye for detail...",
            verbose=verbose
        )

    def create_editing_task(self, story):
        """
        Create a task for editing a story.
        """
        # Implementation here
```

## Testing

You can test the CrewAI integration using the agent playground at `/agents/playground/`.