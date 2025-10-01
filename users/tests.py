from django.test import Client, TestCase
from django.urls import reverse

from users.models import User


# Create your tests here.
class UserRegisterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_register_user_with_unique_valid_data(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
            'password_confirm': 'testpassword'
        }
        )

        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(User.objects.filter(username='testuser').exists())

        user_created = User.objects.get(username='testuser')
        self.assertEqual(user_created.email, 'testuser@example.com')
        self.assertTrue(user_created.check_password('testpassword'))
        self.assertFalse(user_created.check_password('wrongpassword'))
        
    def test_register_user_with_existing_username(self):
        response1 = self.client.post(self.url, {
            'username': 'duplicateuser',
            'email': 'duplicate@example.com',
            'first_name': 'Duplicate',
            'last_name': 'User',
            'password': 'duplicatepassword',
            'password_confirm': 'duplicatepassword'
        })

        self.assertEqual(response1.status_code, 302)  # First registration should succeed

        response2 = self.client.post(self.url, {
            'username': 'duplicateuser',  # Same username
            'email': 'duplicate2@example.com',
            'first_name': 'Duplicate2',
            'last_name': 'User2',
            'password': 'duplicatepassword2',
            'password_confirm': 'duplicatepassword2'
        })

        self.assertEqual(response2.status_code, 200)  # Should return to registration page
        self.assertContains(response2, 'Username already exists.')
        self.assertFalse(User.objects.filter(email='duplicate2@example.com').exists())

    def test_register_user_with_existing_email(self):
        response1 = self.client.post(self.url, {
            'username': 'duplicateEmailUser',
            'email': 'duplicateEmail@example.com',
            'first_name': 'DuplicateEmail',
            'last_name': 'User',
            'password': 'duplicateEmailpassword',
            'password_confirm': 'duplicateEmailpassword'
        })

        self.assertEqual(response1.status_code, 302)  # First registration should succeed

        response2 = self.client.post(self.url, {
            'username': 'duplicateEmailUser2',
            'email': 'duplicateEmail@example.com',
            'first_name': 'DuplicateEmail2',
            'last_name': 'User2',
            'password': 'duplicateEmailpassword2',
            'password_confirm': 'duplicateEmailpassword2'
        })

        self.assertEqual(response2.status_code, 200)  # Should return to registration page
        self.assertContains(response2, 'Email already exists.')
        self.assertFalse(User.objects.filter(username='duplicateEmailUser2').exists())

    def test_register_user_with_mismatched_passwords(self):
        response = self.client.post(self.url, {
            'username': 'passwordMismatchUser',
            'email': 'mismatch@example.com',
            'first_name': 'Mismatch',
            'last_name': 'User',
            'password': 'mismatchpassword',
            'password_confirm': 'differentpassword'
        })

        self.assertEqual(response.status_code, 200)  # Should return to registration page
        self.assertContains(response, 'Passwords do not match.')
        self.assertFalse(User.objects.filter(username='passwordMismatchUser').exists())
