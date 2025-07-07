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
from django.views.decorators.vary import vary_on_headers
from django.views.generic import RedirectView


class ServiceWorkerView(RedirectView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response['Service-Worker-Allowed'] = '/'
        return response


urlpatterns = [
    path('_manifest.json', RedirectView.as_view(url=static('stickymobile/_manifest.json'), permanent=True)),
    path('_service-worker.js', ServiceWorkerView.as_view(
        url=static('stickymobile/_service-worker.js'), permanent=True
    )),

    # Admin
    path("admin/", admin.site.urls),

    # App URLs
    path('stories/', include('talemo.stories.urls')),

    # Redirect root to stories
    path('', RedirectView.as_view(url='/stories/list/', permanent=False)),
]

# Debug toolbar - only for web containers
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
