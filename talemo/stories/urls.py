"""
URL configuration for the stories app.
"""
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'stories'

urlpatterns = [
    path('create/', views.create_story, name='create'),
    path('list/', views.story_list, name='list'),
]
