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
                
                # Add more agent types as needed
                
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