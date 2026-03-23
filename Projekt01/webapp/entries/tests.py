from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import UserProfile
from .models import JournalEntry, MoodCategory, Tag

class EntriesAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 1. Create User A (Our main tester)
        self.user_a = User.objects.create_user(username='alice', password='password123')
        UserProfile.objects.create(user=self.user_a)
        
        # 2. Create User B (To test privacy controls)
        self.user_b = User.objects.create_user(username='bob', password='password123')
        UserProfile.objects.create(user=self.user_b)
        
        # 3. Create Categories and Tags
        self.mood_happy = MoodCategory.objects.create(name="Happy")
        self.mood_sad = MoodCategory.objects.create(name="Sad")
        self.tag_work = Tag.objects.create(name="Work")
        
        # 4. Create an initial entry for User A
        self.entry_a = JournalEntry.objects.create(
            user=self.user_a,
            content="Alice's first entry.",
            mood_score=8,
            mood=self.mood_happy,
            slug="alice-1"
        )
        self.entry_a.tags.add(self.tag_work)
        
        # 5. Create an initial entry for User B
        self.entry_b = JournalEntry.objects.create(
            user=self.user_b,
            content="Bob's secret entry.",
            mood_score=3,
            mood=self.mood_sad,
            slug="bob-1"
        )

        # URLs
        self.list_url = reverse('entries:list')
        self.new_url = reverse('entries:new-entry')
        self.page_url_a = reverse('entries:page', kwargs={'slug': self.entry_a.slug})
        self.edit_url_a = reverse('entries:edit-entry', kwargs={'slug': self.entry_a.slug})
        self.delete_url_a = reverse('entries:delete-entry', kwargs={'slug': self.entry_a.slug})
        
        # User B's URLs
        self.page_url_b = reverse('entries:page', kwargs={'slug': self.entry_b.slug})
        self.edit_url_b = reverse('entries:edit-entry', kwargs={'slug': self.entry_b.slug})

    # --- PRIVACY & ACCESS TESTS ---
    def test_unauthenticated_access_blocked(self):
        """Test that logged-out users cannot access ANY journal pages."""
        urls_to_test = [
            self.list_url, self.new_url, 
            self.page_url_a, self.edit_url_a, self.delete_url_a
        ]
        for url in urls_to_test:
            response = self.client.get(url)
            self.assertRedirects(response, f"/users/login/?next={url}")

    def test_user_cannot_view_others_entries(self):
        """Test that Alice gets a 404 if she tries to view Bob's entry."""
        self.client.login(username='alice', password='password123')
        response = self.client.get(self.page_url_b)
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_edit_others_entries(self):
        """Test that Alice gets a 404 if she tries to edit Bob's entry."""
        self.client.login(username='alice', password='password123')
        response = self.client.get(self.edit_url_b)
        self.assertEqual(response.status_code, 404)

    # --- CRUD LOGIC TESTS ---
    def test_entries_list_view(self):
        """Test the list view only shows the logged-in user's entries."""
        self.client.login(username='alice', password='password123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        # Alice should see her entry, but NOT Bob's
        self.assertContains(response, "Alice&#x27;s first entry") # Django escapes apostrophes
        self.assertNotContains(response, "Bob's secret entry")

    def test_entry_new_custom_slug_logic(self):
        """Test creating a new entry, specifically verifying the custom loop slug logic."""
        self.client.login(username='alice', password='password123')
        
        # Alice already has "alice-1". Creating a new one should generate "alice-2".
        response = self.client.post(self.new_url, {
            'content': "Alice's second entry.",
            'mood_score': 9,
            'mood': self.mood_happy.id,
            'tags': [self.tag_work.id]
        })
        
        self.assertRedirects(response, self.list_url)
        
        # Verify the new entry exists and has the correct incremented slug
        new_entry = JournalEntry.objects.get(slug="alice-2")
        self.assertEqual(new_entry.content, "Alice's second entry.")
        self.assertEqual(new_entry.user, self.user_a)

    def test_entry_new_slug_collision_loop(self):
        """Test the crash-proofing while loop if a slug is somehow taken out of order."""
        self.client.login(username='alice', password='password123')
        
        # Manually create "alice-2" to simulate a weird database state
        JournalEntry.objects.create(
            user=self.user_a, content="Blocker", mood_score=5, slug="alice-2"
        )
        
        # Alice now has 2 entries. Base count + 1 = 3. 
        # But let's say "alice-3" also exists!
        JournalEntry.objects.create(
            user=self.user_a, content="Blocker 2", mood_score=5, slug="alice-3"
        )
        
        # Submit a new form. The loop should skip 1, 2, and 3, and assign "alice-4".
        self.client.post(self.new_url, {
            'content': "Loop test entry.",
            'mood_score': 5,
            'mood': self.mood_happy.id
        })
        
        self.assertTrue(JournalEntry.objects.filter(slug="alice-4").exists())

    def test_entry_edit_view(self):
        """Test updating an existing entry."""
        self.client.login(username='alice', password='password123')
        response = self.client.post(self.edit_url_a, {
            'content': "Alice's UPDATED entry.",
            'mood_score': 10,
            'mood': self.mood_happy.id
        })
        self.assertRedirects(response, self.page_url_a)
        
        self.entry_a.refresh_from_db()
        self.assertEqual(self.entry_a.content, "Alice's UPDATED entry.")
        self.assertEqual(self.entry_a.mood_score, 10)

    def test_entry_delete_view(self):
        """Test deleting an entry."""
        self.client.login(username='alice', password='password123')
        response = self.client.post(self.delete_url_a)
        self.assertRedirects(response, self.list_url)
        
        # Verify it's actually gone from the database
        with self.assertRaises(JournalEntry.DoesNotExist):
            JournalEntry.objects.get(slug="alice-1")