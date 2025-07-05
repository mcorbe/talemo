"""
URL configuration for the assets API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssetViewSet, AssetUsageViewSet

app_name = 'assets_api'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename='asset')
router.register(r'tenant-usage', AssetUsageViewSet, basename='tenant-usage')

urlpatterns = [
    path('', include(router.urls)),
]
