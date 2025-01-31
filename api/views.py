import PyPDF2
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.views.generic.detail import DetailView

from .models import Email
from .utils.categorize import classify_text
from .utils.extract_file import extract_email_subject_message
from .utils.generate_response import generate_response
from .utils.process import process_text


# Create your views here.
@method_decorator(csrf_protect, name='dispatch')
class EmailRegisterView(View):

    def get(self, request):
        return render(request, 'email_register.html')
    
    def post(self, request):
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if 'file' in request.FILES:
            file = request.FILES['file']
            fs = FileSystemStorage(location='media/uploads')
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)

            if file.name.endswith('.txt'):
                with open(f'media/uploads/{filename}', 'r', encoding='utf-8') as f:
                    content = f.read()
            elif file.name.endswith('.pdf'):
                with open(f'media/uploads/{filename}', 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    content = ""
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        content += page.extract_text()
            else:
                messages.error(request, 'Formato de arquivo não suportado. Apenas PDF e TXT são permitidos.')
                return render(request, 'email_register.html')

            content = ' '.join(content.split())
            email, subject, message = extract_email_subject_message(content)
            if not email or not subject or not message:
                messages.error(request, 'Falha ao extrair informações do arquivo.')
                return render(request, 'email_register.html')

        if not email:
            messages.error(request, 'Preencha o email.')
            return render(request, 'email_register.html')
        if not subject:
            messages.error(request, 'Preencha o assunto.')
            return render(request, 'email_register.html', {'form.subject.errors': 'Subject is required.'})
        if not message:
            messages.error(request, 'Preencha o texto do email.')
            return render(request, 'email_register.html', {'form.message.errors': 'Message is required.'})
        
        processed_message = process_text(message)   
        result = classify_text(processed_message)

        email_obj = Email()

        category = "Produtivo" if result == 0 else "Improdutivo"

        response = generate_response(processed_message)

        try:
            email_obj.create_email(email, subject, message, category, response)
        except Exception as e:
            print(e)
            messages.error(request, 'Failed to register email.')
            return render(request, 'email_register.html')

        messages.success(request, 'Email registered successfully.')
        return redirect('index')


class GetEmailsView(View):

    def get(self, request):
        emails = Email().get_emails()
        return render(request, 'index.html', {'emails': emails})
    

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


class AboutView(View):

    def get(self, request):
        return render(request, 'about.html')
    

class ContactView(View):

    def get(self, request):
        return render(request, 'contact.html')