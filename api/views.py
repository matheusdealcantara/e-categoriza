import PyPDF2
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.views.generic.detail import DetailView

from emails.views import EmailDetailView, EmailRegisterView
from www.views import AboutView, ContactView, GetEmailsView

from .models import Email
from .utils.categorize import classify_text
from .utils.extract_file import extract_email_subject_message
from .utils.generate_response import generate_response
from .utils.process import process_text
