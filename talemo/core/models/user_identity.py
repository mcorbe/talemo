"""
User identity models for the core app.
"""
from django.db import models
import uuid


class UserIdentity(models.Model):
    """
    User identity model for the core app.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='identities')
    idp_issuer = models.CharField(max_length=255)
    idp_subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'core_user_identity'
        unique_together = ('idp_issuer', 'idp_subject')

    def __str__(self):
        return f"{self.user.name} - {self.idp_issuer}"