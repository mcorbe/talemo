"""
Views for the stories app.
"""
from django.shortcuts import render, redirect
from .models.story import Story
from .models.chapter import Chapter
from .models.age_group import AgeGroup

# User flow views
def home_copilot(request):
    return render(request, 'stories/home_copilot.html')

def wizard_step1(request):
    return render(request, 'stories/wizard_step1_select_topic.html')

def wizard_step2(request):
    if request.method == 'POST':
        context = {
            'topic': request.POST.get('topic', '')
        }
        return render(request, 'stories/wizard_step2_select_hero.html', context)
    return redirect('stories:wizard_step1')

def wizard_step3(request):
    if request.method == 'POST':
        context = {
            'topic': request.POST.get('topic', ''),
            'hero': request.POST.get('hero', ''),
            'story_id': request.POST.get('story_id', ''),
            'chapter_number': request.POST.get('chapter_number', '1')
        }
        return render(request, 'stories/wizard_step3_select_place.html', context)
    return redirect('stories:wizard_step2')

def wizard_step4(request):
    if request.method == 'POST':
        context = {
            'topic': request.POST.get('topic', ''),
            'hero': request.POST.get('hero', ''),
            'place': request.POST.get('place', ''),
            'story_id': request.POST.get('story_id', ''),
            'chapter_number': request.POST.get('chapter_number', '1')
        }
        return render(request, 'stories/wizard_step4_select_tool.html', context)
    return redirect('stories:wizard_step3')

def generating(request):
    if request.method == 'POST':
        # Store data in session for later use
        request.session['topic'] = request.POST.get('topic', '')
        request.session['hero'] = request.POST.get('hero', '')
        request.session['place'] = request.POST.get('place', '')
        request.session['tool'] = request.POST.get('tool', '')

        # Check if we're creating a new story or a new chapter
        if request.POST.get('story_id'):
            # We're creating a new chapter for an existing story
            request.session['story_id'] = request.POST.get('story_id')
            request.session['chapter_number'] = int(request.POST.get('chapter_number', 1))
        else:
            # We're creating a new story
            request.session['story_id'] = None
            request.session['chapter_number'] = 1

        context = {
            'topic': request.session['topic'],
            'hero': request.session['hero'],
            'place': request.session['place'],
            'tool': request.session['tool'],
            'story_id': request.session.get('story_id'),
            'chapter_number': request.session.get('chapter_number')
        }
        return render(request, 'stories/generating.html', context)
    return redirect('stories:wizard_step4')

def playback(request):
    # In a real implementation, this would retrieve the generated story
    # For now, we'll just pass along the context from the session or a dummy story

    # Create or retrieve the story and chapter
    story_id = request.session.get('story_id')
    chapter_number = request.session.get('chapter_number', 1)

    if story_id:
        # Retrieve existing story
        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            # If story doesn't exist, create a new one
            story_id = None

    if not story_id:
        # Create a new story
        story = Story(
            title=f"{request.session.get('hero', 'a hero')} in {request.session.get('place', 'a place')}",
            description=f"A story about {request.session.get('hero', 'a hero')} using {request.session.get('tool', 'a tool')} in {request.session.get('place', 'a place')}",
            topic=request.session.get('topic', 'adventure'),
            hero=request.session.get('hero', 'brave knight'),
            created_by_id=request.user.id if request.user.is_authenticated else 1  # Default to admin user if not authenticated
        )
        story.save()
        request.session['story_id'] = str(story.id)

    # Create a new chapter
    chapter = Chapter(
        story=story,
        title=f"{request.session.get('hero', 'a hero')} in {request.session.get('place', 'a place')}",
        content=f"A chapter about {request.session.get('hero', 'a hero')} using {request.session.get('tool', 'a tool')} in {request.session.get('place', 'a place')}",
        place=request.session.get('place', 'enchanted forest'),
        tool=request.session.get('tool', 'magic wand'),
        order=chapter_number,
        duration=60  # Default duration in seconds
    )
    chapter.save()

    # Update story's total duration
    story.total_duration = sum(c.duration for c in story.chapters.all())
    story.save()

    context = {
        'story': story,
        'chapter': chapter,
        'topic': request.session.get('topic', 'adventure'),
        'hero': request.session.get('hero', 'brave knight'),
        'place': request.session.get('place', 'enchanted forest'),
        'tool': request.session.get('tool', 'magic wand'),
        'chapter_number': chapter_number
    }
    return render(request, 'stories/playback.html', context)

def end_of_chapter(request):
    """
    Merged view that combines end_of_chapter and wizard_step1 functionality.
    This view shows the completed chapter and provides options to:
    1. Create a new chapter for the current story
    2. Create a new story
    3. End the current story
    It also includes a feedback mechanism with thumbs up/down.
    """
    story_id = request.session.get('story_id')
    chapter_number = request.session.get('chapter_number', 1)

    try:
        story = Story.objects.get(id=story_id)
        chapter = Chapter.objects.get(story=story, order=chapter_number)
    except (Story.DoesNotExist, Chapter.DoesNotExist):
        return redirect('stories:home_copilot')

    # Handle feedback submission if present
    if request.method == 'POST' and 'feedback' in request.POST:
        feedback = request.POST.get('feedback')
        # In a real implementation, this would store the feedback
        # For now, we just acknowledge it and redirect
        if 'next_action' in request.POST:
            next_action = request.POST.get('next_action')
            if next_action == 'new_chapter':
                # Pass the necessary data to wizard_step3
                return render(request, 'stories/wizard_step3_select_place.html', {
                    'topic': request.POST.get('topic', ''),
                    'hero': request.POST.get('hero', ''),
                    'story_id': request.POST.get('story_id', ''),
                    'chapter_number': request.POST.get('chapter_number', '1')
                })
            elif next_action == 'new_story':
                return redirect('stories:wizard_step1')
            elif next_action == 'end_story':
                return redirect('stories:end_of_story')

        # Default redirect if no next_action specified
        return redirect('stories:home_copilot')

    context = {
        'story': story,
        'chapter': chapter,
        'chapter_number': chapter_number
    }
    return render(request, 'stories/end_of_chapter.html', context)

def end_of_story(request):
    story_id = request.session.get('story_id')

    try:
        story = Story.objects.get(id=story_id)
        chapters = Chapter.objects.filter(story=story).order_by('order')
    except Story.DoesNotExist:
        return redirect('stories:home_copilot')

    context = {
        'story': story,
        'chapters': chapters
    }
    return render(request, 'stories/end_of_story.html', context)

def age_groups(request):
    """
    View to display all age groups as cards.
    """
    age_groups = AgeGroup.objects.all()
    context = {
        'age_groups': age_groups
    }
    return render(request, 'stories/age_groups.html', context)
