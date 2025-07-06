"""
Views for the stories app.
"""
from django.shortcuts import render
from .models import Story


def create_story(request):
    return render(request, 'stories/create.html')

def story_list(request):
    return render(request, 'stories/list.html', {
        'stories': Story.objects.all()
    })

