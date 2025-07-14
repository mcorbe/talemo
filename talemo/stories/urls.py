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
    # User flow URLs
    path('home/', views.home_copilot, name='home_copilot'),
    path('wizard/step1/', views.wizard_step1, name='wizard_step1'),
    path('wizard/step2/', views.wizard_step2, name='wizard_step2'),
    path('wizard/step3/', views.wizard_step3, name='wizard_step3'),
    path('wizard/step4/', views.wizard_step4, name='wizard_step4'),
    path('wizard/step5/', views.wizard_step5, name='wizard_step5'),
    path('generating/', views.generating, name='generating'),
    path('playback/', views.playback, name='playback'),
    path('end-of-story/', views.end_of_story, name='end_of_story'),

    # API endpoints
    path('api/check-task-status/', views.check_task_status, name='check_task_status'),
]
