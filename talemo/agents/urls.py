"""
URL configuration for the agents app.
"""
from django.urls import path
from django.views.generic import TemplateView
from talemo.agents.views import playground

app_name = 'agents'

urlpatterns = [
    # Add URL patterns here
    path('', TemplateView.as_view(template_name='agents/index.html'), name='index'),
    path('playground/', playground, name='playground'),
]
