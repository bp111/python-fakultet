from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile
from entries.models import MoodCategory, Tag, JournalEntry, Reflection

class Command(BaseCommand):
    help = 'Populate the db with dummy users, categories, tags, and entries'

    def handle(self, *args, **kwargs):
        self.stdout.write("Database population started...")
        
        moods = ['Jolly', 'Sad', 'Chilling', 'Grumpy']
        tags = ['#keepcalm', '#wokeupwiththeswag', '#downindadumpz:(', '#PIZZA_TIME!!!']

        for mood in moods:
            MoodCategory.objects.get_or_create(name=mood)
        for tag in tags:
            Tag.objects.get_or_create(name=tag)

        self.stdout.write(self.style.SUCCESS('Successfully populated with moods and tags'))
        
        users_data = ['Adam', 'Eve']
        for username in users_data:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password('haslomaslo')
                user.save()
                UserProfile.objects.get_or_create(user=user, desc=f"My bio")
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
        
        user1 = User.objects.get(username='Adam')
        jolly = MoodCategory.objects.get(name='Jolly')
        tag = Tag.objects.get(name='#wokeupwiththeswag')
        
        if not JournalEntry.objects.filter(user=user1).exists():
            entry = JournalEntry.objects.create(
                user=user1,
                content="So very happy and in a jolly mood today.",
                mood_score=150,
                mood=jolly,
                slug="Adam-1"
            )
            entry.tags.add(tag)
                        
            Reflection.objects.create(
                entry=entry,
                notes="Honestly it wasn't that good of a day now that I think of it"
            )
            self.stdout.write(self.style.SUCCESS('Created dummy entries and reflections'))

        self.stdout.write(self.style.SUCCESS('Database population complete'))