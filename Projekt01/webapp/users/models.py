from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    desc = models.TextField(blank=True, help_text="Share some more info about yourself!")
    receive_reminders = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
