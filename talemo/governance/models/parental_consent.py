"""
Parental consent models for the governance app.
"""
from django.db import models
import uuid


class ParentalConsent(models.Model):
    """
    Parental consent model for the governance app.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE, related_name='parental_consents')
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='received_consents')
    consenting_user = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='given_consents')
    consent_type = models.CharField(
        max_length=50,
        choices=[
            ('app_usage', 'App Usage'),
            ('data_processing', 'Data Processing'),
            ('recording', 'Recording'),
        ],
        default='app_usage'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('granted', 'Granted'),
            ('revoked', 'Revoked'),
        ],
        default='granted'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'governance_parental_consent'
        unique_together = ('tenant', 'user', 'consenting_user', 'consent_type')

    def __str__(self):
        return f"{self.consenting_user.name} -> {self.user.name} ({self.consent_type})"