from django.core.management.base import BaseCommand
from entries.models import JournalEntry

class Command(BaseCommand):
    help = 'Wipe all journal entries from the db'

    def handle(self, *args, **kwargs):
        count = JournalEntry.objects.count()        
        if count == 0:
            self.stdout.write(self.style.WARNING("Nothing to wipe - the journal is already empty"))
            return
        
        JournalEntry.objects.all().delete()        
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} journal entries and their reflections'))