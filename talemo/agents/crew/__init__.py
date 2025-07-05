"""
CrewAI integration for the Talemo platform.
"""
from .base import BaseAgent, BaseCrew
from .story_agents import StorytellerAgent, IllustratorAgent as StoryIllustratorAgent, NarratorAgent
from .story_crew import StoryCreationCrew, StoryEnhancementCrew
from .agent_implementations import (
    ModerationAgent,
    TTSAgent,
    IllustratorAgent,
    QuotaAgent,
    EmbeddingAgent,
    StoryCompanion
)

__all__ = [
    'BaseAgent',
    'BaseCrew',
    'StorytellerAgent',
    'StoryIllustratorAgent',  # Renamed to avoid conflict with IllustratorAgent from agent_implementations
    'NarratorAgent',
    'StoryCreationCrew',
    'StoryEnhancementCrew',
    'ModerationAgent',
    'TTSAgent',
    'IllustratorAgent',
    'QuotaAgent',
    'EmbeddingAgent',
    'StoryCompanion',
]
