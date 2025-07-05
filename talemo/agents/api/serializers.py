"""
Serializers for the agents API.
"""
from rest_framework import serializers
from talemo.agents.models.agent_task import AgentTask


class AgentTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the AgentTask model.
    """
    class Meta:
        model = AgentTask
        fields = [
            'id', 'agent_type', 'status', 'input', 'output', 'error',
            'created_at', 'started_at', 'completed_at', 'token_usage', 'model_used'
        ]
        read_only_fields = ['id', 'created_at', 'started_at', 'completed_at']


class AgentTaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an AgentTask.
    """
    class Meta:
        model = AgentTask
        fields = ['agent_type', 'input']


class AgentQuotaSerializer(serializers.Serializer):
    """
    Serializer for agent usage quota information.
    """
    total_tasks = serializers.IntegerField()
    tasks_by_type = serializers.DictField(child=serializers.IntegerField())
    token_usage = serializers.DictField(child=serializers.IntegerField())
    quota_limits = serializers.DictField(child=serializers.IntegerField())
    quota_remaining = serializers.DictField(child=serializers.IntegerField())


class StoryCompanionSerializer(serializers.Serializer):
    """
    Serializer for StoryCompanion agent interactions.
    """
    message = serializers.CharField()
    context = serializers.DictField(required=False)
    
    class Meta:
        fields = ['message', 'context']


class StoryCompanionResponseSerializer(serializers.Serializer):
    """
    Serializer for StoryCompanion agent responses.
    """
    response = serializers.CharField()
    suggestions = serializers.ListField(child=serializers.CharField(), required=False)
    story_elements = serializers.DictField(required=False)
    
    class Meta:
        fields = ['response', 'suggestions', 'story_elements']