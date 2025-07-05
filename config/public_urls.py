"""
URL configuration for the public schema.
This file contains URL patterns that are only accessible from the public schema.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("<h1>Welcome to Talemo Public Tenant</h1>")

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Simple home view for testing
    path('', home_view, name='home'),
]

# Debug toolbar - only for web containers
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
