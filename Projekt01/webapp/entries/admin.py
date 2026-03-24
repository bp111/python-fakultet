from django.contrib import admin
from .models import Tag, MoodCategory, JournalEntry, Reflection

admin.site.register(JournalEntry)
admin.site.register(Tag)
admin.site.register(MoodCategory)
admin.site.register(Reflection)