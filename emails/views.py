from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView

from api.utils import generate_response
from api.utils.categorize import classify_text
from api.utils.generate_response import generate_response
from api.utils.process import process_text
from emails.models import Email


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
            messages.error(request, 'Preencha o email.')
            return render(request, 'email_register.html')
        if not subject:
            messages.error(request, 'Preencha o assunto.')
            return render(request, 'email_register.html', {'form.subject.errors': 'Subject is required.'})
        if not message:
            messages.error(request, 'Preencha o texto do email.')
            return render(request, 'email_register.html', {'form.message.errors': 'Message is required.'})
        
        # Processar o texto
        # processed_message = process_text(message)   

        # Classificar o texto
        result = classify_text(message)

        # Remover pontos e dígitos do resultado
        # result = ''.join([i for i in result if not i.isdigit() and i not in ['.', ',']])

        # Criar objeto de email
        email_obj = Email()

        # Gerar resposta
        response = generate_response(message)

        try:
            # Registrar email
            email_obj.create_email(email, subject, message, result, response)
        except Exception as e:
            print(e)
            messages.error(request, 'Failed to register email.')
            return render(request, 'email_register.html')

        messages.success(request, 'Email registered successfully.')
        return redirect('index')

class EmailDetailView(DetailView):
    model = Email
    template_name = 'email_detail.html'
    context_object_name = 'email'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return Email().get_email(id_)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
