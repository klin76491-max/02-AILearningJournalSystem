from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from accounts.services import GoogleAuthService
from inventory.models import MentalInventoryItem


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            first_name='Test Learner'
        )
        MentalInventoryItem.objects.create(
            user=self.user,
            content='測試人生清單',
            is_focus=True
        )

    def test_login_page_renders_successfully(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, 'Google')

    def test_authenticated_user_redirected_from_login(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:login'))
        self.assertRedirects(response, reverse('journal:today'))

    def test_google_auth_service_get_auth_url(self):
        with patch('django.conf.settings.GOOGLE_OAUTH_CLIENT_ID', 'dummy-client-id'):
            url = GoogleAuthService.get_auth_url(state='xyz123')
            self.assertIn('https://accounts.google.com/o/oauth2/v2/auth', url)
            self.assertIn('client_id=dummy-client-id', url)

    def test_get_or_create_google_user_new(self):
        profile = {
            'id': '123456789',
            'email': 'newlearner@gmail.com',
            'name': 'New Learner'
        }
        user = GoogleAuthService.get_or_create_google_user(profile)
        self.assertEqual(user.email, 'newlearner@gmail.com')
        self.assertEqual(user.first_name, 'New Learner')

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('accounts:login'))
        self.assertFalse('_auth_user_id' in self.client.session)
