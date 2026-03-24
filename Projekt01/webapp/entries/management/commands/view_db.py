from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from entries.models import JournalEntry, MoodCategory, Tag

class Command(BaseCommand):
    help = 'Display a quick summary of the db records'

    def handle(self, *args, **kwargs):
        u_num = User.objects.count()
        e_num = JournalEntry.objects.count()
        t_num = Tag.objects.count()
        m_num = MoodCategory.objects.count()

        self.stdout.write(self.style.WARNING('\nDATABASE SUMMARY'))
        self.stdout.write(f"Number of Users:      {u_num}")
        self.stdout.write(f"Number of Entries:    {e_num}")
        self.stdout.write(f"Number of Tags:       {t_num}")
        self.stdout.write(f"Number of Moods:      {m_num}")  
        self.stdout.write()        

        if e_num > 0:
            self.stdout.write(self.style.SUCCESS('LATEST 5 ENTRIES'))
            for entry in JournalEntry.objects.order_by('-entry_date')[:5]:
                mood = entry.mood.name if entry.mood else "Unknown"
                content = (entry.content[:30] + '...') if len(entry.content) > 30 else entry.content
                
                self.stdout.write(
                    f"[{entry.entry_date.strftime('%Y-%m-%d')}] "
                    f"User: {entry.user.username} | "
                    f"Mood: {mood} ({entry.mood_score}/10) | "
                    f"Content: \"{content}\""
                )
        self.stdout.write("\n")