"""
URL configuration for the stories app.
"""
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'stories'

urlpatterns = [
    # Add URL patterns here
    path('', TemplateView.as_view(template_name='stories/index.html'), name='index'),

    # Story player with Mode Conte feature
    path('player/', views.story_player, name='player'),
    path('player/<uuid:story_id>/', views.story_player, name='player_with_id'),
]
