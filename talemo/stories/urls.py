"""
URL configuration for the stories app.
"""
from django.urls import path
from django.views.generic import TemplateView

app_name = 'stories'

urlpatterns = [
    # Add URL patterns here
    path('', TemplateView.as_view(template_name='stories/index.html'), name='index'),
]