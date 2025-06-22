"""
Base classes for CrewAI integration.
"""
from crewai import Agent, Task, Crew
from django.conf import settings
import logging
import os
from langfuse.client import Langfuse

logger = logging.getLogger(__name__)

# Initialize Langfuse client if enabled
langfuse_client = None
if settings.LANGTRACE_ENABLED:
    try:
        langfuse_client = Langfuse(
            public_key=settings.LANGFUSE_PUBLIC_KEY,
            secret_key=settings.LANGFUSE_SECRET_KEY,
            host=settings.LANGTRACE_HOST
        )
        logger.info("Langfuse client initialized for LLM observability")
    except Exception as e:
        logger.error(f"Failed to initialize Langfuse client: {e}")
        langfuse_client = None

class BaseAgent:
    """
    Base class for all CrewAI agents.
    """
    def __init__(self, name, role, goal, backstory=None, verbose=True):
        """
        Initialize a base agent.

        Args:
            name (str): The name of the agent
            role (str): The role of the agent
            goal (str): The goal of the agent
            backstory (str, optional): The backstory of the agent
            verbose (bool, optional): Whether to enable verbose logging
        """
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory or f"You are {name}, a {role} with the goal to {goal}."
        self.verbose = verbose
        self._agent = None

    @property
    def agent(self):
        """
        Get the CrewAI agent instance.

        Returns:
            Agent: The CrewAI agent instance
        """
        if self._agent is None:
            self._agent = Agent(
                name=self.name,
                role=self.role,
                goal=self.goal,
                backstory=self.backstory,
                verbose=self.verbose,
                allow_delegation=False,
                llm=self._get_llm()
            )
        return self._agent

    def _get_llm(self):
        """
        Get the language model to use for the agent.

        Returns:
            LLM: The language model instance
        """
        # Default to using OpenAI
        from openai import OpenAI

        api_key = settings.OPENAI_API_KEY
        if not api_key:
            logger.warning("No OpenAI API key found in settings. Using default CrewAI LLM.")
            return None

        # Create the OpenAI client
        client = OpenAI(api_key=api_key)

        # If Langfuse is enabled, wrap the client with tracing
        if settings.LANGTRACE_ENABLED and langfuse_client:
            try:
                # Wrap the client with Langfuse tracing
                from langfuse.openai import openai as langfuse_openai

                # Configure Langfuse to use our OpenAI client
                langfuse_openai.openai = client

                # Return the wrapped client
                logger.info(f"OpenAI client wrapped with Langfuse tracing for agent {self.name}")
                return langfuse_openai
            except Exception as e:
                logger.error(f"Failed to wrap OpenAI client with Langfuse: {e}")
                # Fall back to the unwrapped client
                return client

        # Return the unwrapped client if Langfuse is not enabled
        return client


class BaseCrew:
    """
    Base class for all CrewAI crews.
    """
    def __init__(self, agents, tasks=None, verbose=True):
        """
        Initialize a base crew.

        Args:
            agents (list): List of BaseAgent instances
            tasks (list, optional): List of Task instances
            verbose (bool, optional): Whether to enable verbose logging
        """
        self.agents = agents
        self.tasks = tasks or []
        self.verbose = verbose
        self._crew = None

    @property
    def crew(self):
        """
        Get the CrewAI crew instance.

        Returns:
            Crew: The CrewAI crew instance
        """
        if self._crew is None:
            self._crew = Crew(
                agents=[agent.agent for agent in self.agents],
                tasks=self.tasks,
                verbose=self.verbose
            )
        return self._crew

    def run(self):
        """
        Run the crew.

        Returns:
            str: The result of the crew's work
        """
        # If Langfuse is enabled, trace the crew execution
        if settings.LANGTRACE_ENABLED and langfuse_client:
            try:
                # Create a trace for the crew execution
                trace = langfuse_client.trace(
                    name=f"crew_execution",
                    metadata={
                        "crew_agents": [agent.name for agent in self.agents],
                        "tasks": [task.description[:100] + "..." for task in self.tasks]
                    }
                )

                # Execute the crew with tracing
                with trace.span(name="crew_kickoff"):
                    result = self.crew.kickoff()

                # Log the result
                trace.update(
                    output=result[:500] + "..." if len(result) > 500 else result
                )

                return result
            except Exception as e:
                logger.error(f"Error during traced crew execution: {e}")
                # Fall back to untraced execution
                return self.crew.kickoff()

        # Execute without tracing if Langfuse is not enabled
        return self.crew.kickoff()

    def add_task(self, task):
        """
        Add a task to the crew.

        Args:
            task (Task): The task to add
        """
        self.tasks.append(task)
        # Reset crew to rebuild with new tasks
        self._crew = None
