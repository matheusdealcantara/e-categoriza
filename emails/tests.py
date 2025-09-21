from django.test import Client, TestCase
from django.urls import reverse

from .models import Email


class EmailRegisterViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('email_register')

    def test_get_email_register_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'email_register.html')

    def test_post_email_register_view_success(self):
        data = {
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(Email.objects.filter(email='test@example.com').exists())

    def test_post_email_register_view_missing_email(self):
        data = {
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'email_register.html')
        self.assertContains(response, 'Preencha o email.')

    def test_post_email_register_view_missing_subject(self):
        data = {
            'email': 'test@example.com',
            'message': 'Test Message'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'email_register.html')
        self.assertContains(response, 'Preencha o assunto.')

    def test_post_email_register_view_missing_message(self):
        data = {
            'email': 'test@example.com',
            'subject': 'Test Subject'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'email_register.html')
        self.assertContains(response, 'Preencha o corpo do email.')