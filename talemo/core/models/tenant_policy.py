from django.db import models
from django.utils.translation import gettext_lazy as _

from .tenant import Tenant


class TenantPolicy(models.Model):
    """
    Policy settings for a tenant.
    """
    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name="policy",
        verbose_name=_("Tenant")
    )
    max_users = models.PositiveIntegerField(_("Maximum users"), default=10)
    allow_public_registration = models.BooleanField(_("Allow public registration"), default=False)
    require_email_verification = models.BooleanField(_("Require email verification"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Tenant Policy")
        verbose_name_plural = _("Tenant Policies")

    def __str__(self):
        return f"Policy for {self.tenant.name}"