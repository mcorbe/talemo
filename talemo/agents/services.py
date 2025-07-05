"""
Services for the agents app.
"""
import logging
from datetime import datetime
from django.utils import timezone
from talemo.agents.models import AgentTask
from talemo.agents.crew import StoryCreationCrew, StoryEnhancementCrew
import redis
from django.conf import settings
import json

logger = logging.getLogger(__name__)

# Initialize Redis client for agent communication
redis_client = redis.Redis.from_url(settings.REDIS_URL)

class AgentBridge:
    """
    Bridge between Django and CrewAI for agent tasks.
    """

    @staticmethod
    def create_task(agent_type, input_data, tenant):
        """
        Create a new agent task.

        Args:
            agent_type (str): The type of agent to use
            input_data (dict): The input data for the task
            tenant: The tenant for the task

        Returns:
            AgentTask: The created task
        """
        task = AgentTask(
            agent_type=agent_type,
            status='pending',
            input=input_data,
            tenant=tenant
        )
        task.save()

        # Publish task to Redis for agent communication
        redis_client.publish(
            f'agent_tasks:{agent_type}',
            json.dumps({
                'task_id': str(task.id),
                'tenant_id': str(tenant.id),
                'agent_type': agent_type,
                'input': input_data
            })
        )

        logger.info(f"Created agent task: {task.id} for agent: {agent_type}")
        return task

    @staticmethod
    def update_task_status(task_id, status, output=None, error=None, token_usage=None, model_used=None):
        """
        Update the status of an agent task.

        Args:
            task_id (str): The ID of the task to update
            status (str): The new status of the task
            output (dict, optional): The output data for the task
            error (str, optional): The error message if the task failed
            token_usage (dict, optional): The token usage data
            model_used (str, optional): The model used for the task

        Returns:
            AgentTask: The updated task
        """
        try:
            task = AgentTask.objects.get(id=task_id)
            task.status = status

            if status == 'processing' and not task.started_at:
                task.started_at = timezone.now()

            if status in ['completed', 'failed']:
                task.completed_at = timezone.now()

            if output:
                task.output = output

            if error:
                task.error = error

            if token_usage:
                task.token_usage = token_usage

            if model_used:
                task.model_used = model_used

            task.save()
            logger.info(f"Updated agent task: {task_id} status: {status}")
            return task
        except AgentTask.DoesNotExist:
            logger.error(f"Agent task not found: {task_id}")
            return None

    @staticmethod
    def get_task(task_id):
        """
        Get an agent task by ID.

        Args:
            task_id (str): The ID of the task to get

        Returns:
            AgentTask: The task
        """
        try:
            return AgentTask.objects.get(id=task_id)
        except AgentTask.DoesNotExist:
            logger.error(f"Agent task not found: {task_id}")
            return None

    @staticmethod
    def execute_task(task_id):
        """
        Execute an agent task.

        Args:
            task_id (str): The ID of the task to execute

        Returns:
            dict: The result of the task
        """
        try:
            task = AgentTask.objects.get(id=task_id)

            # Update task status to processing
            AgentBridge.update_task_status(task_id, 'processing')

            # Execute the task based on agent type
            result = None
            token_usage = {}
            model_used = None

            try:
                if task.agent_type == 'StoryCompanion':
                    # Create a story creation crew
                    crew = StoryCreationCrew(verbose=True)

                    # Generate the story
                    result = crew.create_story(
                        prompt=task.input.get('prompt', ''),
                        age_range=task.input.get('age_range', '4-8'),
                        user_id=task.input.get('user_id'),
                        tenant_id=str(task.tenant.id)
                    )

                    # Extract token usage if available
                    if hasattr(crew, 'token_usage'):
                        token_usage = crew.token_usage

                    # Extract model used if available
                    if hasattr(crew, 'model_used'):
                        model_used = crew.model_used

                elif task.agent_type == 'ModerationAgent':
                    # Import the ModerationAgent
                    from talemo.agents.crew import ModerationAgent

                    # Create a moderation agent
                    agent = ModerationAgent(verbose=True)

                    # Create and execute the moderation task
                    moderation_task = agent.create_moderation_task(
                        content=task.input.get('content', ''),
                        age_range=task.input.get('age_range', '4-8')
                    )

                    # Execute the task
                    result = agent.agent.execute_task(moderation_task)

                elif task.agent_type == 'TTSAgent':
                    # Import the TTSAgent
                    from talemo.agents.crew import TTSAgent

                    # Create a TTS agent
                    agent = TTSAgent(verbose=True)

                    # Create and execute the TTS task
                    tts_task = agent.create_tts_task(
                        text=task.input.get('text', ''),
                        voice_params=task.input.get('voice_params', {})
                    )

                    # Execute the task
                    result = agent.agent.execute_task(tts_task)

                elif task.agent_type == 'IllustratorAgent':
                    # Import the IllustratorAgent
                    from talemo.agents.crew import IllustratorAgent

                    # Create an illustrator agent
                    agent = IllustratorAgent(verbose=True)

                    # Create and execute the illustration task
                    illustration_task = agent.create_illustration_task(
                        story=task.input.get('story', '')
                    )

                    # Execute the task
                    result = agent.agent.execute_task(illustration_task)

                elif task.agent_type == 'QuotaAgent':
                    # Import the QuotaAgent
                    from talemo.agents.crew import QuotaAgent

                    # Create a quota agent
                    agent = QuotaAgent(verbose=True)

                    # Create and execute the quota check task
                    quota_task = agent.create_quota_check_task(
                        tenant_id=str(task.tenant.id),
                        resource_type=task.input.get('resource_type', ''),
                        requested_amount=task.input.get('requested_amount', 1)
                    )

                    # Execute the task
                    result = agent.agent.execute_task(quota_task)

                elif task.agent_type == 'EmbeddingAgent':
                    # Import the EmbeddingAgent
                    from talemo.agents.crew import EmbeddingAgent

                    # Create an embedding agent
                    agent = EmbeddingAgent(verbose=True)

                    # Create and execute the embedding task
                    embedding_task = agent.create_embedding_task(
                        content=task.input.get('content', ''),
                        embedding_type=task.input.get('embedding_type', 'story')
                    )

                    # Execute the task
                    result = agent.agent.execute_task(embedding_task)

                # Extract token usage and model used if available for individual agents
                if 'agent' in locals() and hasattr(agent, 'agent'):
                    if hasattr(agent.agent, 'token_usage'):
                        token_usage = agent.agent.token_usage
                    if hasattr(agent.agent, 'model_used'):
                        model_used = agent.agent.model_used

                # Update task status to completed
                AgentBridge.update_task_status(
                    task_id, 
                    'completed', 
                    output=result,
                    token_usage=token_usage,
                    model_used=model_used
                )

                return result

            except Exception as e:
                # Update task status to failed
                AgentBridge.update_task_status(task_id, 'failed', error=str(e))
                logger.error(f"Error executing agent task: {task_id} - {str(e)}")
                raise

        except AgentTask.DoesNotExist:
            logger.error(f"Agent task not found: {task_id}")
            return None
