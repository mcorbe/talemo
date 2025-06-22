"""
Core app configuration.
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configuration for the core app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'talemo.core'
    verbose_name = 'Core'

    def ready(self):
        """
        Import signals when the app is ready.
        """
        import talemo.core.signals  # noqa