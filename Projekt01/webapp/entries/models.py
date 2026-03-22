from django.db import models

class JournalEntry(models.Model):
    content = models.TextField()
    entry_date = models.DateTimeField(auto_now_add=True)
    mood_score = models.IntegerField(null=True)
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return self.entry_date.strftime("%Y-%m-%d %H:%M:%S")
