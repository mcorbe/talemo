from django.urls import path
from .views import start_audio_session, task_status
urlpatterns = [
    path("start/", start_audio_session, name="start-audio"),
    path("task-status/<str:task_id>/", task_status, name="task-status"),
]
