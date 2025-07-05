"""
Views for the agents API.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Count
from django.utils import timezone
from talemo.agents.models.agent_task import AgentTask
from .serializers import (
    AgentTaskSerializer,
    AgentTaskCreateSerializer,
    AgentQuotaSerializer,
    StoryCompanionSerializer,
    StoryCompanionResponseSerializer
)


class AgentTaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for agent tasks.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        This view should return a list of all agent tasks for the currently authenticated user's tenant.
        """
        return AgentTask.objects.filter(tenant=self.request.tenant)
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create' or self.action == 'trigger':
            return AgentTaskCreateSerializer
        return AgentTaskSerializer
    
    def perform_create(self, serializer):
        """
        Set the tenant when creating an agent task.
        """
        serializer.save(tenant=self.request.tenant)
    
    @action(detail=False, methods=['post'])
    def trigger(self, request):
        """
        Trigger an agent task.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(tenant=request.tenant)
        
        # In a real implementation, this would trigger the agent task
        # For now, we'll just return the task ID
        
        return Response({
            'task_id': task.id,
            'status': 'pending'
        }, status=status.HTTP_202_ACCEPTED)


class AgentQuotaViewSet(viewsets.ViewSet):
    """
    API endpoint for agent usage quota information.
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """
        Get agent usage quota information for the current tenant.
        """
        # Get total number of tasks
        tasks = AgentTask.objects.filter(tenant=request.tenant)
        total_tasks = tasks.count()
        
        # Get tasks by type
        tasks_by_type = tasks.values('agent_type').annotate(count=Count('id'))
        tasks_by_type_dict = {item['agent_type']: item['count'] for item in tasks_by_type}
        
        # Get token usage
        # In a real implementation, this would calculate token usage from the token_usage field
        # For now, we'll just return placeholder data
        token_usage = {
            'total': 1000000,
            'ModerationAgent': 200000,
            'TTSAgent': 300000,
            'IllustratorAgent': 500000
        }
        
        # Get quota limits
        # In a real implementation, this would come from TenantPolicy
        # For now, we'll just return placeholder data
        quota_limits = {
            'total': 5000000,
            'ModerationAgent': 1000000,
            'TTSAgent': 1500000,
            'IllustratorAgent': 2500000
        }
        
        # Calculate remaining quota
        quota_remaining = {
            key: quota_limits.get(key, 0) - token_usage.get(key, 0)
            for key in set(quota_limits.keys()) | set(token_usage.keys())
        }
        
        data = {
            'total_tasks': total_tasks,
            'tasks_by_type': tasks_by_type_dict,
            'token_usage': token_usage,
            'quota_limits': quota_limits,
            'quota_remaining': quota_remaining
        }
        
        serializer = AgentQuotaSerializer(data)
        return Response(serializer.data)


class StoryCompanionView(APIView):
    """
    API endpoint for interacting with the StoryCompanion agent.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Interact with the StoryCompanion agent.
        """
        serializer = StoryCompanionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        message = serializer.validated_data['message']
        context = serializer.validated_data.get('context', {})
        
        # In a real implementation, this would call the StoryCompanion agent
        # For now, we'll just return a placeholder response
        
        # Create a task to track the interaction
        task = AgentTask.objects.create(
            tenant=request.tenant,
            agent_type='StoryCompanion',
            status='completed',
            input={
                'message': message,
                'context': context
            },
            output={
                'response': f"I'd love to help you with a story about {message}!",
                'suggestions': [
                    f"How about a story set in a magical forest?",
                    f"Would you like a story with talking animals?",
                    f"Maybe a story about a brave child on an adventure?"
                ],
                'story_elements': {
                    'theme': 'adventure',
                    'characters': ['child', 'magical creature'],
                    'setting': 'forest'
                }
            },
            started_at=timezone.now(),
            completed_at=timezone.now()
        )
        
        response_serializer = StoryCompanionResponseSerializer(task.output)
        return Response(response_serializer.data)