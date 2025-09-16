from django.shortcuts import render
from django.views import View

from emails.models import Email


# Create your views here.
class GetEmailsView(View):

    def get(self, request):
        email_obj = Email()
        emails = email_obj.get_emails()
        return render(request, 'index.html', {'emails': emails})

class AboutView(View):

    def get(self, request):
        return render(request, 'about.html')
    

class ContactView(View):

    def get(self, request):
        return render(request, 'contact.html')