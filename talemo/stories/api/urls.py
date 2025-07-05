"""
URL configuration for the stories API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StoryViewSet, TagViewSet, StorySearchView

app_name = 'stories_api'

router = DefaultRouter()
router.register(r'stories', StoryViewSet, basename='story')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'search', StorySearchView, basename='search')

urlpatterns = [
    path('', include(router.urls)),
]
