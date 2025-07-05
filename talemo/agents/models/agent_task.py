"""
Agent task model for storing agent task information.
"""
from django.db import models
import uuid
import json
from django_tenants.models import TenantMixin


class AgentTask(TenantMixin):
    """
    Model for storing agent task information.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_type = models.CharField(
        max_length=50,
        choices=[
            ('ModerationAgent', 'Moderation Agent'),
            ('TTSAgent', 'TTS Agent'),
            ('IllustratorAgent', 'Illustrator Agent'),
            ('QuotaAgent', 'Quota Agent'),
            ('EmbeddingAgent', 'Embedding Agent'),
            ('StoryCompanion', 'Story Companion'),
        ]
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    input = models.JSONField(default=dict)
    output = models.JSONField(default=dict, null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    token_usage = models.JSONField(default=dict, null=True, blank=True)
    model_used = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        app_label = 'agents'

    def __str__(self):
        return f"{self.agent_type} - {self.status} - {self.id}"

    def set_input(self, input_data):
        """
        Set the input data for the task.

        Args:
            input_data (dict): The input data for the task
        """
        self.input = input_data
        self.save()

    def set_output(self, output_data):
        """
        Set the output data for the task.

        Args:
            output_data (dict): The output data for the task
        """
        self.output = output_data
        self.save()

    def set_error(self, error_message):
        """
        Set the error message for the task.

        Args:
            error_message (str): The error message
        """
        self.error = error_message
        self.status = 'failed'
        self.save()

    def set_token_usage(self, token_usage):
        """
        Set the token usage for the task.

        Args:
            token_usage (dict): The token usage data
        """
        self.token_usage = token_usage
        self.save()
