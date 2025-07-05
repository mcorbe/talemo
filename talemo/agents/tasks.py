"""
Celery tasks for the agents app.
"""
from talemo.agents.services import AgentBridge

from celery import shared_task
from django.conf import settings
from django.utils import timezone

import logging
import json
import redis

logger = logging.getLogger(__name__)

# Initialize Redis client for agent communication
redis_client = redis.Redis.from_url(settings.REDIS_URL)

@shared_task
def generate_story(prompt, age_range="4-8", user_id=None, tenant_id=None):
    """
    Generate a complete story with illustrations and narration.

    Args:
        prompt (str): The story prompt or theme
        age_range (str, optional): The target age range for the story
        user_id (str, optional): The ID of the user creating the story
        tenant_id (str, optional): The ID of the tenant

    Returns:
        dict: A dictionary containing the task ID and status
    """
    logger.info(f"Generating story with prompt: {prompt}, age range: {age_range}")

    try:
        # Create the agent task
        task = AgentBridge.create_task(
            agent_type='StoryCompanion',
            input_data={
                'prompt': prompt,
                'age_range': age_range,
                'user_id': user_id
            }
        )

        # Execute the task asynchronously
        execute_agent_task.delay(str(task.id))

        logger.info(f"Story generation task created: {task.id}")
        return {
            'task_id': str(task.id),
            'status': task.status
        }
    except Exception as e:
        logger.error(f"Error creating story generation task: {str(e)}")
        raise

@shared_task
def enhance_story(story, user_id=None, tenant_id=None):
    """
    Enhance an existing story with illustrations and narration.

    Args:
        story (str): The existing story text
        user_id (str, optional): The ID of the user enhancing the story
        tenant_id (str, optional): The ID of the tenant

    Returns:
        dict: A dictionary containing the task ID and status
    """
    logger.info(f"Enhancing story: {story[:100]}...")

    try:
        # Create the agent task
        task = AgentBridge.create_task(
            agent_type='StoryEnhancement',
            input_data={
                'story': story,
                'user_id': user_id
            }
        )

        # Execute the task asynchronously
        execute_agent_task.delay(str(task.id))

        logger.info(f"Story enhancement task created: {task.id}")
        return {
            'task_id': str(task.id),
            'status': task.status
        }
    except Exception as e:
        logger.error(f"Error creating story enhancement task: {str(e)}")
        raise

@shared_task
def execute_agent_task(task_id):
    """
    Execute an agent task.

    Args:
        task_id (str): The ID of the task to execute

    Returns:
        dict: The result of the task
    """
    logger.info(f"Executing agent task: {task_id}")

    try:
        # Execute the task
        result = AgentBridge.execute_task(task_id)

        # Publish the result to Redis
        redis_client.publish(
            f'agent_results:{task_id}',
            json.dumps({
                'task_id': task_id,
                'status': 'completed',
                'result': result
            })
        )

        logger.info(f"Agent task executed successfully: {task_id}")
        return result
    except Exception as e:
        # Publish the error to Redis
        redis_client.publish(
            f'agent_results:{task_id}',
            json.dumps({
                'task_id': task_id,
                'status': 'failed',
                'error': str(e)
            })
        )

        logger.error(f"Error executing agent task: {task_id} - {str(e)}")
        raise

@shared_task
def process_agent_queue():
    """
    Process the agent task queue.

    This task is scheduled to run periodically to check for pending tasks.
    """
    logger.info("Processing agent task queue")

    try:
        # Get all pending tasks
        from talemo.agents.models import AgentTask
        pending_tasks = AgentTask.objects.filter(status='pending')

        for task in pending_tasks:
            # Execute the task asynchronously
            execute_agent_task.delay(str(task.id))

            logger.info(f"Scheduled pending task for execution: {task.id}")

        return f"Processed {pending_tasks.count()} pending tasks"
    except Exception as e:
        logger.error(f"Error processing agent task queue: {str(e)}")
        raise
