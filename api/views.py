from django.contrib import messages
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View

from .models import Email


# Create your views here.
@method_decorator(csrf_protect, name='dispatch')
class EmailRegisterView(View):

    def get(self, request):
        return render(request, 'email_register.html')
    
    def post(self, request):
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not email:
            messages.error(request, 'Email is required.')
            return render(request, 'email_register.html')
            # return render(request, 'email_register.html', {'form.email.errors': 'Email is required.'}, )
        if not subject:
            messages.error(request, 'Subject is required.')
            return render(request, 'email_register.html', {'form.subject.errors': 'Subject is required.'})
        if not message:
            messages.error(request, 'Message is required.')
            return render(request, 'email_register.html', {'form.message.errors': 'Message is required.'})

        email_obj = Email()

        try:
            email_obj.create_email(email, subject, message)
        except Exception as e:
            print(e)
            messages.error(request, 'Failed to register email.')
            return render(request, 'email_register.html')

        messages.success(request, 'Email registered successfully.')
        return render(request, 'email_register.html')


class GetEmailsView(View):

    def get(self, request):
        emails = Email().get_emails()
        return render(request, 'index.html', {'emails': emails})