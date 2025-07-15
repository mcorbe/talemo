"""
Views for the stories app.
"""
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from celery.result import AsyncResult
from .models.story import Story
from .models.chapter import Chapter
from .tasks import test_task

# User flow views
def home_copilot(request):
    return render(request, 'stories/home_copilot.html')

def wizard_step1(request):
    # Clear previous wizard session data when starting a new wizard
    keys_to_clear = ['age_group', 'topic', 'hero', 'place', 'tool', 'story_id', 'chapter_number']
    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]

    context = {}

    return render(request, 'stories/wizard_step1_select_age_group.html', context)

def wizard_step2(request):
    if request.method == 'POST':
        # Store data in session
        request.session['age_group'] = request.POST.get('age_group', '')

        # Delete session keys from later steps
        keys_to_delete = ['topic', 'hero', 'place', 'tool', 'story_id', 'chapter_number']
        for key in keys_to_delete:
            if key in request.session:
                del request.session[key]

    # For both GET and POST, render the form with data from the session
    context = {
        'age_group': request.session.get('age_group', '')
    }

    # If we don't have an age group yet, redirect to step 1
    if not context['age_group']:
        return redirect('stories:wizard_step1')

    return render(request, 'stories/wizard_step2_select_topic.html', context)

def wizard_step3(request):
    if request.method == 'POST':
        # Store data in session
        request.session['topic'] = request.POST.get('topic', '')

        # Delete session keys from later steps
        keys_to_delete = ['hero', 'place', 'tool', 'story_id', 'chapter_number']
        for key in keys_to_delete:
            if key in request.session:
                del request.session[key]

    # For both GET and POST, render the form with data from the session
    context = {
        'age_group': request.session.get('age_group', ''),
        'topic': request.session.get('topic', '')
    }

    # If we don't have required data yet, redirect to the appropriate step
    if not context['age_group']:
        return redirect('stories:wizard_step1')
    if not context['topic']:
        return redirect('stories:wizard_step2')

    return render(request, 'stories/wizard_step3_select_hero.html', context)

def wizard_step4(request):
    if request.method == 'POST':
        # Store data in session
        request.session['hero'] = request.POST.get('hero', '')

        # Delete session keys from later steps
        keys_to_delete = ['place', 'tool', 'story_id', 'chapter_number']
        for key in keys_to_delete:
            if key in request.session:
                del request.session[key]

    # For both GET and POST, render the form with data from the session
    context = {
        'age_group': request.session.get('age_group', ''),
        'topic': request.session.get('topic', ''),
        'hero': request.session.get('hero', ''),
    }

    # If we don't have required data yet, redirect to the appropriate step
    if not context['age_group']:
        return redirect('stories:wizard_step1')
    if not context['topic']:
        return redirect('stories:wizard_step2')
    if not context['hero']:
        return redirect('stories:wizard_step3')

    return render(request, 'stories/wizard_step4_select_place.html', context)

def wizard_step5(request):
    if request.method == 'POST':
        # Store data in session
        request.session['place'] = request.POST.get('place', '')

    # For both GET and POST, render the form with data from the session
    context = {
        'age_group': request.session.get('age_group', ''),
        'topic': request.session.get('topic', ''),
        'hero': request.session.get('hero', ''),
        'place': request.session.get('place', ''),
        'story_id': request.session.get('story_id', ''),
        'chapter_number': request.session.get('chapter_number', '')
    }

    # If we don't have required data yet, redirect to the appropriate step
    if not context['age_group']:
        return redirect('stories:wizard_step1')
    if not context['topic']:
        return redirect('stories:wizard_step2')
    if not context['hero']:
        return redirect('stories:wizard_step3')
    if not context['place']:
        return redirect('stories:wizard_step4')

    return render(request, 'stories/wizard_step5_select_tool.html', context)

def generating(request):
    if request.method == 'POST':
        # Store data in session for later use
        request.session['tool'] = request.POST.get('tool', '')

    # For both GET and POST, prepare context from session
    context = {
        'age_group': request.session.get('age_group', ''),
        'topic': request.session.get('topic', ''),
        'hero': request.session.get('hero', ''),
        'place': request.session.get('place', ''),
        'tool': request.session.get('tool', ''),
        'story_id': request.session.get('story_id', ''),
        'chapter_number': request.session.get('chapter_number', '')
    }

    # If we don't have required data yet, redirect to the appropriate step
    if not context['age_group']:
        return redirect('stories:wizard_step1')
    if not context['topic']:
        return redirect('stories:wizard_step2')
    if not context['hero']:
        return redirect('stories:wizard_step3')
    if not context['place']:
        return redirect('stories:wizard_step4')
    if not context['tool']:
        return redirect('stories:wizard_step5')

    # Check if we already have a task_id in the session
    task_id = request.session.get('story_task_id')

    # If this is a new request or we don't have a task_id, start a new task
    if request.method == 'POST' or not task_id:
        from .services import generate_story_chapter

        # Prepare the JSON input for the story generation task
        json_input = {
            "story": {
                "age_group": context['age_group'],
                "topic": context['topic'],
                "hero": context['hero'],
                "chapters": [
                    {
                        "place": context['place'],
                        "tool": context['tool'],
                        "order": 1
                    }
                ]
            }
        }

        # Start the Celery task
        task_result = generate_story_chapter(json_input)

        # Store the task ID in the session
        request.session['story_task_id'] = task_result.id
        context['task_id'] = task_result.id

    return render(request, 'stories/generating.html', context)

def playback(request):
    # Retrieve the generated story using the story_id and chapter_number from the session

    # For both GET and POST, prepare context from session
    context = {
        'age_group': request.session.get('age_group', ''),
        'topic': request.session.get('topic', ''),
        'hero': request.session.get('hero', ''),
        'place': request.session.get('place', ''),
        'tool': request.session.get('tool', ''),
        'story_id': request.session.get('story_id', ''),
        'chapter_number': request.session.get('chapter_number', '')
    }

    # If we don't have required data yet, redirect to the appropriate step
    if not context['age_group']:
        return redirect('stories:wizard_step1')
    if not context['topic']:
        return redirect('stories:wizard_step2')
    if not context['hero']:
        return redirect('stories:wizard_step3')
    if not context['place']:
        return redirect('stories:wizard_step4')
    if not context['tool']:
        return redirect('stories:wizard_step5')

    # Check if we have a task_id in the session
    task_id = request.session.get('story_task_id')

    # If we have a task_id, check if the task is complete
    if task_id:
        from celery.result import AsyncResult
        task_result = AsyncResult(task_id)

        # If the task is still running, redirect back to the generating page
        if not task_result.ready():
            return redirect('stories:generating')

    story = None

    # Try to retrieve the existing story
    if context['story_id']:
        try:
            story = Story.objects.get(id=context['story_id'])
        except Story.DoesNotExist:
            # If the story doesn't exist, clear the story_id
            context['story_id'] = None
            request.session['story_id'] = None

    # If we don't have a story yet, create one
    if not story:
        # Create a new story
        story = Story(
            title=f"{context['hero']} in {context['place']}",
            description=f"A story about {context['hero']} using {context['tool']} in {context['place']}",
            topic=context['topic'],
            hero=context['hero'],
            age_group=context['age_group'],
        )
        story.save()

        request.session['story_id'] = str(story.id)
        context['story_id'] = request.session['story_id']

    # Get the chapter
    chapter = None
    chapter_number = context.get('chapter_number', 1)

    try:
        # Try to retrieve the existing chapter
        chapter = Chapter.objects.get(story=story, order=chapter_number)
    except Chapter.DoesNotExist:
        # If the chapter doesn't exist, create a new one
        chapter = Chapter(
            story=story,
            title=f"Chapter {chapter_number}",
            content=f"A chapter about {context['hero']} using {context['tool']} in {context['place']}",
            place=context['place'],
            tool=context['tool'],
            order=int(chapter_number) if chapter_number else 1,
        )
        chapter.save()

    # Add the chapter to the context
    context['chapter'] = chapter

    # Clear the task_id from the session
    if 'story_task_id' in request.session:
        del request.session['story_task_id']

    return render(request, 'stories/playback.html', context)

def end_of_story(request):
    story_id = request.session.get('story_id')

    try:
        story = Story.objects.get(id=story_id)
        chapters = Chapter.objects.filter(story=story).order_by('order')
    except Story.DoesNotExist:
        return redirect('stories:home_copilot')

    context = {
        'story': story,
        'chapters': chapters,
        'age_group': request.session.get('age_group', '')
    }
    return render(request, 'stories/end_of_story.html', context)

def check_task_status(request):
    """
    Check the status of a Celery task and return it as JSON.
    """
    task_id = request.GET.get('task_id')
    if not task_id:
        return JsonResponse({'status': 'error', 'message': 'No task ID provided'})

    # Get the task result
    task_result = AsyncResult(task_id)

    # Check if task is ready
    if not task_result.ready():
        # Task is still running
        return JsonResponse({
            'status': 'pending',
            'progress': 'Story generation in progress...'
        })

    # Check if task is in success
    if not task_result.successful():
        # Task failed
        return JsonResponse({
            'status': 'complete',
            'result': 'error',
            'error': str(task_result.result)
        })

    # Task completed successfully
    result = task_result.get()

    # Store the story and chapter IDs in the session
    if result and isinstance(result, dict):
        # The task result contains the chapter data and story ID
        # We'll store them in the session so the playback view can use them

        # Store the story ID in the session
        if 'story_id' in result:
            request.session['story_id'] = result['story_id']

        # Store the chapter number in the session
        if 'order' in result:
            request.session['chapter_number'] = result['order']

    return JsonResponse({
        'status': 'complete',
        'result': 'success',
        'redirect': '/stories/playback/'
    })