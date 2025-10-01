from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView


# Create your views here.
class LoginView(View):
    def get(self, request):
        user_session = request.session.get('user')
        if user_session:
            return render(request, 'index.html')
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        return render(request, 'login.html', {'error': 'Invalid credentials'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

@method_decorator(csrf_protect, name='dispatch')   
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')


        if not all([username, email, first_name, last_name, password, password_confirm]):
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'register.html')

        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return redirect('login')

class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'user_profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self):
        username = self.kwargs.get(self.slug_url_kwarg)
        return get_user_model().objects.get(username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.get_object()

        return context

    def get(self, request, *args, **kwargs):
        user_session = request.session.get('user')
        if not user_session:
            return redirect('login')
        return super().get(request, *args, **kwargs)
