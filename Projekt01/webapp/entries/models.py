from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class MoodCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    tags = models.ManyToManyField(Tag, blank=True)
    mood = models.ForeignKey(MoodCategory, on_delete=models.SET_NULL, null=True)

    content = models.TextField()
    entry_date = models.DateTimeField(auto_now_add=True)
    mood_score = models.IntegerField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"My entry from {self.entry_date.strftime('%Y-%m-%d')}"

class Reflection(models.Model):    
    entry = models.OneToOneField(JournalEntry, on_delete=models.CASCADE, related_name='reflection')
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reflection on {self.entry}"