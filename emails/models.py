from django.db import models
from django.db.models import Q

# Create your models here.

class Email(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email
    
    def get_emails(self):
        return Email.objects.all()
    
    def get_email(self, email_id):
        email_obj = Email.objects.get(pk=email_id)
        return email_obj
    
    def create_email(self, email, subject, message, category=None, response=None):
        new_email = Email(email=email, subject=subject, message=message, category=category, response=response)
        new_email.save()
        return new_email

    def delete_email(self, email_id):
        email_obj = Email.objects.get(pk=email_id)
        email_obj.delete()
        return email_obj