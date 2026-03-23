from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['desc', 'receive_reminders']
        labels = {
            'desc': 'About me',
            'receive_reminders': 'Send me daily reminders to keep writing :)'
        }