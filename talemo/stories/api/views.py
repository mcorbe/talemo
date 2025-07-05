"""
Views for the stories API.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from talemo.stories.models.story import Story
from talemo.stories.models.tag import Tag
from .serializers import (
    StorySerializer, 
    StoryCreateSerializer, 
    StoryUpdateSerializer, 
    StoryVisibilitySerializer,
    TagSerializer
)


class StoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for stories.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['visibility', 'age_range', 'language', 'is_published', 'is_ai_generated']
    search_fields = ['title', 'description', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        This view should return a list of all stories for the currently authenticated user's tenant.
        """
        return Story.objects.filter(tenant=self.request.tenant)

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return StoryCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return StoryUpdateSerializer
        elif self.action == 'visibility':
            return StoryVisibilitySerializer
        return StorySerializer

    @action(detail=True, methods=['patch'])
    def visibility(self, request, pk=None):
        """
        Update the visibility of a story.
        """
        story = self.get_object()
        serializer = self.get_serializer(story, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Set the tenant and created_by when creating a story.
        """
        serializer.save(tenant=self.request.tenant)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for tags (read-only).
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name']

    def get_queryset(self):
        """
        This view should return a list of all tags for the currently authenticated user's tenant.
        """
        return Tag.objects.filter(tenant=self.request.tenant)


class StorySearchView(viewsets.ViewSet):
    """
    API endpoint for searching stories.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Search for stories based on query parameters.
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {"error": "Search query is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Basic search implementation - can be enhanced with vector search later
        stories = Story.objects.filter(
            tenant=request.tenant,
            title__icontains=query
        ) | Story.objects.filter(
            tenant=request.tenant,
            description__icontains=query
        ) | Story.objects.filter(
            tenant=request.tenant,
            content__icontains=query
        )
        
        # Apply filters if provided
        age_range = request.query_params.get('age_range')
        if age_range:
            stories = stories.filter(age_range=age_range)
            
        visibility = request.query_params.get('visibility')
        if visibility:
            stories = stories.filter(visibility=visibility)
        
        # Ensure distinct results
        stories = stories.distinct()
        
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data)