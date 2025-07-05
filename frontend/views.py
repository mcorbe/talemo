from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.conf import settings
import os

@cache_control(max_age=43200)  # Cache for 12 hours
def service_worker(request):
    """
    Serve the service worker file from the root path.
    This is necessary for the service worker to have the correct scope.
    """
    # Get the path to the service worker file
    service_worker_path = os.path.join(settings.STATIC_ROOT, 'pwa', 'service-worker.js')

    # If the file doesn't exist in the static root (e.g., in development),
    # use the file from the static directory
    if not os.path.exists(service_worker_path):
        service_worker_path = os.path.join(settings.BASE_DIR, 'frontend', 'static', 'pwa', 'service-worker.js')

    # Read the file content
    with open(service_worker_path, 'r') as f:
        content = f.read()

    # Return the content with the correct content type
    return HttpResponse(content, content_type='application/javascript')

@cache_control(max_age=43200)  # Cache for 12 hours
def offline(request):
    """
    Serve the offline page.
    """
    return render(request, 'offline.html')
