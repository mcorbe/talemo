"""
URL configuration for the governance API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParentalConsentViewSet, ParentalControlsView, ChildActivityView

app_name = 'governance_api'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'parental-consent', ParentalConsentViewSet, basename='parental-consent')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),

    # Class-based views
    path('parental-controls/', ParentalControlsView.as_view(), name='parental-controls'),
    path('activity/', ChildActivityView.as_view(), name='child-activity'),
]
