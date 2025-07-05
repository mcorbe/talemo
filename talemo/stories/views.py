"""
Views for the story_list app.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Story

@login_required
def story_list(request):
    story_list = Story.objects.all()
    return render(request, 'story_list/index.html', {'story_list': story_list})