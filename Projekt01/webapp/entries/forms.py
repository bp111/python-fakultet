from django import forms
from .models import JournalEntry, Reflection

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['content', 'mood_score', 'mood', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

class ReflectionForm(forms.ModelForm):
    class Meta:
        model = Reflection
        fields = ['notes']
        labels = {
            'notes': 'How do you remember that time?'
        }