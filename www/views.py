from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from emails.models import Email


# Create your views here.
class GetEmailsView(LoginRequiredMixin, View):

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
    

class HomeView(View):
    
    def get(self, request):
        return render(request, 'home.html')