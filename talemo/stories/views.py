"""
Views for the stories app.
"""
from django.shortcuts import render, redirect
from .models import Story

# User flow views
def home_copilot(request):
    return render(request, 'stories/home_copilot.html')

def wizard_step1(request):
    return render(request, 'stories/wizard_step1.html')

def wizard_step2(request):
    if request.method == 'POST':
        context = {
            'topic': request.POST.get('topic', '')
        }
        return render(request, 'stories/wizard_step2.html', context)
    return redirect('stories:wizard_step1')

def wizard_step3(request):
    if request.method == 'POST':
        context = {
            'topic': request.POST.get('topic', ''),
            'hero': request.POST.get('hero', '')
        }
        return render(request, 'stories/wizard_step3.html', context)
    return redirect('stories:wizard_step2')

def wizard_step4(request):
    if request.method == 'POST':
        context = {
            'topic': request.POST.get('topic', ''),
            'hero': request.POST.get('hero', ''),
            'place': request.POST.get('place', '')
        }
        return render(request, 'stories/wizard_step4.html', context)
    return redirect('stories:wizard_step3')

def generating(request):
    if request.method == 'POST':
        # Store data in session for later use
        request.session['topic'] = request.POST.get('topic', '')
        request.session['hero'] = request.POST.get('hero', '')
        request.session['place'] = request.POST.get('place', '')
        request.session['tool'] = request.POST.get('tool', '')

        context = {
            'topic': request.session['topic'],
            'hero': request.session['hero'],
            'place': request.session['place'],
            'tool': request.session['tool']
        }
        return render(request, 'stories/generating.html', context)
    return redirect('stories:wizard_step4')

def playback(request):
    # In a real implementation, this would retrieve the generated story
    # For now, we'll just pass along the context from the session or a dummy story
    context = {
        'topic': request.session.get('topic', 'adventure'),
        'hero': request.session.get('hero', 'brave knight'),
        'place': request.session.get('place', 'enchanted forest'),
        'tool': request.session.get('tool', 'magic wand')
    }
    return render(request, 'stories/playback.html', context)

def end_of_story(request):
    return render(request, 'stories/end_of_story.html')
