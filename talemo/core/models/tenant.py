from django.db import models
from django.utils.translation import gettext_lazy as _


class Tenant(models.Model):
    """
    Tenant model for multi-tenancy support.
    """
    schema_name = models.CharField(_("Schema Name"), max_length=63, unique=True, db_index=True)
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    type = models.CharField(_("Type"), max_length=50, default='family')
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")

    def __str__(self):
        return self.name


class Domain(models.Model):
    """
    Domain model for mapping domains to tenants.
    """
    domain = models.CharField(_("Domain"), max_length=253, unique=True)
    tenant = models.ForeignKey(
        Tenant, 
        on_delete=models.CASCADE, 
        related_name="domains",
        verbose_name=_("Tenant")
    )
    is_primary = models.BooleanField(_("Primary"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Domain")
        verbose_name_plural = _("Domains")

    def __str__(self):
        return self.domain
