"""
URL configuration for the assets app.
"""
from django.urls import path
from django.views.generic import TemplateView

app_name = 'assets'

urlpatterns = [
    # Add URL patterns here
    path('', TemplateView.as_view(template_name='assets/index.html'), name='index'),
]