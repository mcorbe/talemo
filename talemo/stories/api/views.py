"""
Views for the stories API.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from talemo.stories.models.story import Story
from talemo.stories.models.tag import Tag
from .serializers import (
    StorySerializer, 
    StoryCreateSerializer, 
    StoryUpdateSerializer, 
    StoryVisibilitySerializer,
    TagSerializer
)


@extend_schema(tags=['stories'])
class StoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing stories.

    Stories are the core content of the Talemo platform, containing text, audio, and images.
    This viewset provides CRUD operations for stories, with tenant-based isolation.
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

    @extend_schema(
        summary="Update story visibility",
        description="Update the visibility of a story (public, tenant_only, or private).",
        request=StoryVisibilitySerializer,
        responses={200: StoryVisibilitySerializer},
        examples=[
            OpenApiExample(
                'Public visibility',
                summary='Make a story public',
                value={'visibility': 'public'},
                request_only=True,
            ),
            OpenApiExample(
                'Tenant-only visibility',
                summary='Make a story visible only to tenant members',
                value={'visibility': 'tenant_only'},
                request_only=True,
            ),
            OpenApiExample(
                'Private visibility',
                summary='Make a story private (creator only)',
                value={'visibility': 'private'},
                request_only=True,
            ),
        ]
    )
    @action(detail=True, methods=['patch'])
    def visibility(self, request, pk=None):
        """
        Update the visibility of a story.

        Changes who can access the story:
        - public: Anyone can access
        - tenant_only: Only members of the same tenant can access
        - private: Only the creator can access
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


@extend_schema(
    tags=['stories'],
    parameters=[
        OpenApiParameter(
            name='category',
            description='Filter tags by category (theme, character, mood, setting, age_range, other)',
            required=False,
            type=str,
            enum=['theme', 'character', 'mood', 'setting', 'age_range', 'other'],
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='search',
            description='Search tags by name',
            required=False,
            type=str,
            location=OpenApiParameter.QUERY
        ),
    ],
    responses={200: TagSerializer(many=True)}
)
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for tags (read-only).

    Tags are used to categorize stories and enable filtering and discovery.
    This viewset provides read-only access to tags, with tenant-based isolation.
    Tags are organized by categories such as theme, character, mood, etc.
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


@extend_schema(
    tags=['stories'],
    parameters=[
        OpenApiParameter(
            name='q',
            description='Search query string',
            required=True,
            type=str,
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='age_range',
            description='Filter by age range (e.g., 0-3, 4-6, 7-9, 10-12, 13+)',
            required=False,
            type=str,
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='visibility',
            description='Filter by visibility (public, tenant_only, private)',
            required=False,
            type=str,
            enum=['public', 'tenant_only', 'private'],
            location=OpenApiParameter.QUERY
        ),
    ],
    responses={200: StorySerializer(many=True)}
)
class StorySearchView(viewsets.ViewSet):
    """
    API endpoint for searching stories.

    This endpoint allows searching for stories by text query, with optional filters
    for age range and visibility. The search is performed across title, description,
    and content fields.
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
