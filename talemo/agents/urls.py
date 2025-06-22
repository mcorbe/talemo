"""
URL configuration for the agents app.
"""
from django.urls import path
from django.views.generic import TemplateView

app_name = 'agents'

urlpatterns = [
    # Add URL patterns here
    path('', TemplateView.as_view(template_name='agents/index.html'), name='index'),
    path('playground/', TemplateView.as_view(template_name='agents/playground.html'), name='playground'),
]