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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from frontend.views import service_worker, offline

# API URL patterns
api_patterns = [
    # Include API URLs for each app
    path('core/', include('talemo.core.api.urls')),
    path('stories/', include('talemo.stories.api.urls')),
    path('agents/', include('talemo.agents.api.urls')),
    path('assets/', include('talemo.assets.api.urls')),
    path('governance/', include('talemo.governance.api.urls')),
    path('subscriptions/', include('talemo.subscriptions.api.urls')),
]

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API
    path('api/v1/', include(api_patterns)),

    # App URLs
    path('stories/', include('talemo.stories.urls')),
    path('agents/', include('talemo.agents.urls')),
    path('assets/', include('talemo.assets.urls')),

    # PWA URLs - must be at root level for service worker scope
    path('service-worker.js', service_worker, name='service_worker'),
    path('offline/', offline, name='offline'),

    # Redirect root to stories
    path('', RedirectView.as_view(url='/stories/', permanent=False)),
]

# Add API Documentation URLs only in web containers
urlpatterns += [
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Debug toolbar - only for web containers
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
