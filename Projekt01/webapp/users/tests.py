from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile

class UsersAppTests(TestCase):
    def setUp(self):
        # Set up a test client and a test user
        self.client = Client()
        self.signup_url = reverse('users:signup')
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')
        self.profile_url = reverse('users:profile')
        
        # Create a user for testing login and profile
        self.test_user = User.objects.create_user(
            username='testuser', 
            password='testpassword123'
        )
        # Create the profile (since our app logic currently creates it in the signup view, 
        # manually created test users need it created here)
        self.test_profile = UserProfile.objects.create(user=self.test_user, desc="Initial bio")

    # --- MODEL TESTS ---
    def test_user_profile_str(self):
        """Test the string representation of the UserProfile model."""
        self.assertEqual(str(self.test_profile), "testuser's Profile")

    # --- VIEW TESTS: SIGNUP ---
    def test_signup_view_get(self):
        """Test that the signup page loads correctly."""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_signup_view_post_success(self):
        """Test successful signup creates a user AND a UserProfile, then redirects."""
        # Using exact field names and a strong password to pass Django's built-in validation
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'SuperSecretPassword123!', 
            'password2': 'SuperSecretPassword123!',
        })
        
        # Should redirect to entries list
        self.assertRedirects(response, reverse('entries:list'))
        
        # Check if user was created
        new_user = User.objects.get(username='newuser')
        self.assertIsNotNone(new_user)
        
        # Check if the custom logic created the UserProfile
        self.assertTrue(UserProfile.objects.filter(user=new_user).exists())

    # --- VIEW TESTS: LOGIN & LOGOUT ---
    def test_login_view_get(self):
        """Test that the login page loads correctly."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post_success(self):
        """Test that a user can log in with valid credentials."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertRedirects(response, reverse('entries:list'))

    def test_logout_view(self):
        """Test that logging out redirects to the home page."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, '/')

    # --- VIEW TESTS: PROFILE (ACCESS & EDITING) ---
    def test_profile_view_unauthenticated(self):
        """Test that unauthenticated users are redirected to the login page."""
        response = self.client.get(self.profile_url)
        # Should redirect to login page with the 'next' parameter
        self.assertRedirects(response, f"/users/login/?next={self.profile_url}")

    def test_profile_view_get_authenticated(self):
        """Test that logged-in users can view their profile page."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_view_post_update(self):
        """Test that a user can update their profile information."""
        self.client.login(username='testuser', password='testpassword123')
        
        response = self.client.post(self.profile_url, {
            'desc': 'This is my updated test bio!',
        })
        
        self.assertRedirects(response, self.profile_url)
        self.test_profile.refresh_from_db()
        self.assertEqual(self.test_profile.desc, 'This is my updated test bio!')