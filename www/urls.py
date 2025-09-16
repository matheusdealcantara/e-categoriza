from django.urls import path

from .views import AboutView, ContactView, GetEmailsView

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('', GetEmailsView.as_view(), name='get_emails'),
]