
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from .forms import CustomAuthenticationForm

class HomeMainView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request, *args, **kwargs):
        """Renderuje formularz logowania."""
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Obsługuje logowanie po przesłaniu formularza."""
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})