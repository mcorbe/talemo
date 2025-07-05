"""
Subscription models for the subscriptions app.
"""
from django.db import models
import uuid


class Subscription(models.Model):
    """
    Subscription model for the subscriptions app.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE, related_name='subscriptions')
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.CharField(
        max_length=50,
        choices=[
            ('free', 'Free'),
            ('creator_premium', 'Creator Premium'),
        ],
        default='free'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('canceled', 'Canceled'),
            ('expired', 'Expired'),
        ],
        default='active'
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    payment_provider = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'subscriptions_subscription'

    def __str__(self):
        return f"{self.tenant.name} - {self.plan} ({self.status})"