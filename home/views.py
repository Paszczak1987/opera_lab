
from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomAuthenticationForm

class HomeMainView(TemplateView):
    template_name = 'home/home.html'
    
class LoginView(TemplateView):
    template_name = 'home/login.html'
    
    def get(self, request, *args, **kwargs):
        """Renderuje formularz logowania."""
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Obsługuje logowanie po przesłaniu formularza."""
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home:logged_in')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class WelcomeView(TemplateView):
    template_name = 'home/logged_in.html'

    def get(self, request, *args, **kwargs):
        role_redirects = {
            'admin': 'users:admin_dashboard',
            'client': 'users:client_dashboard',
            'manager': 'users:manager_dashboard',
            'technician': 'users:technician_dashboard',
            'viewer': 'users:viewer_dashboard',
        }
        target = role_redirects.get(getattr(request.user, 'role', None))
        if target:
            return redirect(target)
        return super().get(request, *args, **kwargs)

def logout_view(request):
    logout(request)
    return redirect('home:home')
