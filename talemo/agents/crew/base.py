"""
Base classes for CrewAI integration.
"""
from crewai import Agent, Task, Crew
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

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
            
        return OpenAI(api_key=api_key)


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