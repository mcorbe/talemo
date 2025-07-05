from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    # Serve the service worker from the root path
    path('service-worker.js', views.service_worker, name='service_worker'),
    
    # Serve the offline page
    path('offline/', views.offline, name='offline'),
]