"""
Views for the stories app.
"""
from django.shortcuts import render, redirect
from .models.story import Story
from .models.chapter import Chapter

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

    return render(request, 'stories/generating.html', context)

def playback(request):
    # In a real implementation, this would retrieve the generated story
    # For now, we'll just pass along the context from the session or a dummy story

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


    story = None


    if context['story_id']:
        try:
            # Retrieve the existing story
            story = Story.objects.get(id=context['story_id'])
        except Story.DoesNotExist:
            # If the story doesn't exist, create a new one
            context['story_id'] = None

    if not context['story_id']:
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

    # Create a new chapter
    if not context['chapter_number']:
        chapter = Chapter(
            story=story,
            content=f"A chapter about {context['hero']} using {context['tool']} in {context['place']}",
            place=context['place'],
            tool=context['tool'],
            order=context['chapter_number'] if context['chapter_number'] else 1,
        )
        chapter.save()

        request.session['chapter_number'] = str(chapter.order)
        context['chapter_number'] = request.session['chapter_number']

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
