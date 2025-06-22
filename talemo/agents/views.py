"""
Views for the agents app.
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging
from .tasks import generate_story, enhance_story

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def generate_story_api(request):
    """
    API endpoint to generate a story.
    
    Expects a JSON body with:
    - prompt: The story prompt or theme
    - age_range: (optional) The target age range for the story
    
    Returns a JSON response with:
    - task_id: The ID of the Celery task
    """
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt')
        age_range = data.get('age_range', '4-8')
        
        if not prompt:
            return JsonResponse({'error': 'Prompt is required'}, status=400)
        
        # Start the Celery task
        task = generate_story.delay(prompt, age_range)
        
        return JsonResponse({'task_id': task.id})
    except Exception as e:
        logger.error(f"Error in generate_story_api: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def enhance_story_api(request):
    """
    API endpoint to enhance a story.
    
    Expects a JSON body with:
    - story: The existing story text
    
    Returns a JSON response with:
    - task_id: The ID of the Celery task
    """
    try:
        data = json.loads(request.body)
        story = data.get('story')
        
        if not story:
            return JsonResponse({'error': 'Story is required'}, status=400)
        
        # Start the Celery task
        task = enhance_story.delay(story)
        
        return JsonResponse({'task_id': task.id})
    except Exception as e:
        logger.error(f"Error in enhance_story_api: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def task_status(request, task_id):
    """
    Check the status of a Celery task.
    
    Args:
        task_id: The ID of the Celery task
        
    Returns a JSON response with:
    - status: The status of the task
    - result: The result of the task (if completed)
    """
    from celery.result import AsyncResult
    
    task = AsyncResult(task_id)
    
    response = {
        'task_id': task_id,
        'status': task.status,
    }
    
    if task.status == 'SUCCESS':
        response['result'] = task.result
    elif task.status == 'FAILURE':
        response['error'] = str(task.result)
    
    return JsonResponse(response)

def playground(request):
    """
    Render the agent playground page.
    """
    return render(request, 'agents/playground.html')