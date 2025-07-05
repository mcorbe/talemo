"""
URL configuration for the agents API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from talemo.agents.views import generate_story_api, enhance_story_api, task_status
from .views import AgentTaskViewSet, AgentQuotaViewSet, StoryCompanionView

app_name = 'agents_api'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'tasks', AgentTaskViewSet, basename='task')
router.register(r'quota', AgentQuotaViewSet, basename='quota')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),

    # Existing function-based views
    path('generate-story/', generate_story_api, name='generate_story'),
    path('enhance-story/', enhance_story_api, name='enhance_story'),
    path('task-status/<str:task_id>/', task_status, name='task_status'),

    # New class-based views
    path('story-companion/', StoryCompanionView.as_view(), name='story_companion'),
    path('trigger/', AgentTaskViewSet.as_view({'post': 'trigger'}), name='trigger'),
]
