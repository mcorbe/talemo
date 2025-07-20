"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    # Sticky Mobile
    path('_manifest.json', RedirectView.as_view(url=static('stickymobile/_manifest.json'), permanent=True)),

    # Admin
    path("admin/", admin.site.urls),

    # App URLs
    path('stories/', include('talemo.stories.urls')),
    path("audiostream/", include("talemo.audiostream.urls")),

    # Templates
    path('frontend/templates/demo_audio.html', TemplateView.as_view(template_name='demo_audio.html'), name='demo_audio'),

    # Redirect root to home_copilot
    path('', RedirectView.as_view(url='/stories/home/', permanent=False)),
]

# Debug toolbar - only for web containers
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Try to serve HLS files from the Docker container path first
    docker_hls_dir = "/app/media/hls"
    if os.path.exists(docker_hls_dir) and os.path.isdir(docker_hls_dir):
        print(f"Serving HLS files from Docker container path: {docker_hls_dir}")
        urlpatterns += static(settings.HLS_URL, document_root=docker_hls_dir)
        # Also serve without trailing slash
        urlpatterns += static(settings.HLS_URL.rstrip('/'), document_root=docker_hls_dir)

    # Serve HLS files from the media/hls directory in development
    hls_dir = os.path.join(settings.MEDIA_ROOT, 'hls')
    if os.path.exists(hls_dir):
        print(f"Serving HLS files from media/hls directory: {hls_dir}")
        urlpatterns += static(settings.HLS_URL, document_root=hls_dir)
        # Also serve without trailing slash
        urlpatterns += static(settings.HLS_URL.rstrip('/'), document_root=hls_dir)

    # Serve HLS files from the temporary directory if it exists
    # This is a fallback for when the media/hls directory is not writable
    import tempfile
    temp_dir = tempfile.gettempdir()
    for dir_name in os.listdir(temp_dir):
        if dir_name.startswith('hls_'):
            hls_temp_dir = os.path.join(temp_dir, dir_name)
            if os.path.isdir(hls_temp_dir):
                print(f"Serving HLS files from temporary directory: {hls_temp_dir}")
                # Serve with the standard HLS URL
                # Look for session directories inside the temp directory
                for session_dir in os.listdir(hls_temp_dir):
                    session_path = os.path.join(hls_temp_dir, session_dir)
                    if os.path.isdir(session_path):
                        # Map /media/hls/{session_id}/ to {hls_temp_dir}/{session_id}/
                        print(f"Mapping /media/hls/{session_dir}/ to {session_path}")
                        # Add URL pattern with trailing slash
                        urlpatterns += static(f"/media/hls/{session_dir}/", document_root=session_path)
                        # Add URL pattern without trailing slash to handle both cases
                        urlpatterns += static(f"/media/hls/{session_dir}", document_root=session_path)

                # Also serve the root temp directory with the standard HLS URL for new sessions
                urlpatterns += static(settings.HLS_URL, document_root=hls_temp_dir)
                # Also serve without trailing slash
                urlpatterns += static(settings.HLS_URL.rstrip('/'), document_root=hls_temp_dir)

                # Also serve with an alternative URL for direct access
                urlpatterns += static(f"/temp_hls/{dir_name}/", document_root=hls_temp_dir)
                # Also serve without trailing slash
                urlpatterns += static(f"/temp_hls/{dir_name}", document_root=hls_temp_dir)
