from django.db import models
from django.db.models import Q

# Create your models here.

class Email(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.email
    
    def get_emails(self):
        return Email.objects.all()
    
    def get_email(self, email_id):
        return Email.objects.get(pk=email_id)
    
    def create_email(self, email, subject, message):
        new_email = Email(email=email, subject=subject, message=message)
        new_email.save()
        return new_email

    def update_email(self, email_id, email=None, subject=None, message=None):
        email_obj = Email.objects.get(pk=email_id)
        if email:
            email_obj.email = email
        if subject:
            email_obj.subject = subject
        if message:
            email_obj.message = message
        email_obj.save()
        return email_obj

    def delete_email(self, email_id):
        email_obj = Email.objects.get(pk=email_id)
        email_obj.delete()
        return email_obj