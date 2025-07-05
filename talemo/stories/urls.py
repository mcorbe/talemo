"""
URL configuration for the story_list app.
"""
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'story_list'

urlpatterns = [
    path('', views.story_list, name='index'),
]
