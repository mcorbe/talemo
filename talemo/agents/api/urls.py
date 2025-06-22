"""
URL configuration for the agents API.
"""
from django.urls import path
from talemo.agents.views import generate_story_api, enhance_story_api, task_status

app_name = 'agents_api'

urlpatterns = [
    path('generate-story/', generate_story_api, name='generate_story'),
    path('enhance-story/', enhance_story_api, name='enhance_story'),
    path('task-status/<str:task_id>/', task_status, name='task_status'),
]
