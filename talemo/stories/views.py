"""
Views for the stories app.
"""
from django.shortcuts import render
from .models import Story

def story_list(request):
    return render(request, 'stories/index.html', {
        'stories': Story.objects.all()
    })