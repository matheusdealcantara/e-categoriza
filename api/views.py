from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View


# Create your views here.
@method_decorator(csrf_protect, name='dispatch')
class EmailRegisterView(View):

    def get(self, request):
        return render(request, 'email_register.html')
    
    def post(self, request):
        email = request.POST.get('email')
        print(email)
        return render(request, 'email_register.html')
