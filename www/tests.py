from django.test import Client, TestCase
from django.urls import reverse

from emails.models import Email
from tests.orchestrator import clear_database, create_test_user


# Create your tests here.
class GetEmailsViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        clear_database()
        self.user = create_test_user()
        self.client.force_login(self.user)
        self.url = reverse('index')
        self.email = Email.objects.create(email='test@example.com', subject='Test Subject', message='Test Message')

    def test_get_emails_view_not_authenticated(self):
        unauthenticated_client = Client()
        response = unauthenticated_client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_get_emails_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, self.email.email)