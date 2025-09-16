from django.urls import path

from .views import EmailDetailView, EmailRegisterView

urlpatterns = [
    path("register/", EmailRegisterView.as_view(), name='email_register'),
    path("<int:id>/", EmailDetailView.as_view(), name='email_detail'),
]