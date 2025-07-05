"""
Views for the governance API.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from talemo.governance.models.parental_consent import ParentalConsent
from .serializers import (
    ParentalConsentSerializer,
    ParentalConsentCreateSerializer,
    ParentalConsentUpdateSerializer,
    ParentalControlSettingsSerializer,
    ChildActivitySerializer
)


class ParentalConsentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for parental consents.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        This view should return a list of all parental consents for the currently authenticated user's tenant.
        """
        # Only return consents where the current user is the consenting user (parent)
        return ParentalConsent.objects.filter(
            tenant=self.request.tenant,
            consenting_user=self.request.user
        )
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return ParentalConsentCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return ParentalConsentUpdateSerializer
        return ParentalConsentSerializer


class ParentalControlsView(APIView):
    """
    API endpoint for parental control settings.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get parental control settings.
        """
        # In a real implementation, this would fetch settings from TenantPolicy
        # For now, we'll just return placeholder data
        settings = {
            'max_age_range': '7-9',
            'content_filters': ['violence', 'scary'],
            'time_limits': {
                'weekday': 60,  # minutes
                'weekend': 120  # minutes
            }
        }
        
        serializer = ParentalControlSettingsSerializer(settings)
        return Response(serializer.data)
    
    def put(self, request):
        """
        Update parental control settings.
        """
        serializer = ParentalControlSettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # In a real implementation, this would update settings in TenantPolicy
        # For now, we'll just return the validated data
        
        return Response(serializer.validated_data)


class ChildActivityView(APIView):
    """
    API endpoint for child activity reports.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get child activity report.
        """
        # In a real implementation, this would fetch activity data from a tracking system
        # For now, we'll just return placeholder data
        
        # Get child user ID from query params
        child_id = request.query_params.get('child_id')
        if not child_id:
            return Response(
                {"error": "child_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the child belongs to the current user's tenant
        # In a real implementation, this would also check if the current user is the parent
        
        activity = {
            'user_id': child_id,
            'user_name': 'Child Name',
            'stories_viewed': [
                {
                    'id': '123e4567-e89b-12d3-a456-426614174000',
                    'title': 'The Magic Forest',
                    'duration': 300,  # seconds
                    'timestamp': '2023-06-15T14:30:00Z'
                },
                {
                    'id': '223e4567-e89b-12d3-a456-426614174000',
                    'title': 'The Brave Knight',
                    'duration': 240,  # seconds
                    'timestamp': '2023-06-15T15:00:00Z'
                }
            ],
            'total_time': 540,  # seconds
            'activity_by_day': {
                '2023-06-15': 540,
                '2023-06-14': 300,
                '2023-06-13': 420
            }
        }
        
        serializer = ChildActivitySerializer(activity)
        return Response(serializer.data)