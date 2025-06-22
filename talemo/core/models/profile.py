"""
User profile models.
"""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    User profile model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_parent = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_profile'

    def __str__(self):
        return f"{self.user.username}'s profile"
