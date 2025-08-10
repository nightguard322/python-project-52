from django.contrib.auth.views import LoginView
from .forms import CrispyLoginForm
from django.urls import reverse_lazy

class CrispyLoginView(LoginView):
    form_class = CrispyLoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('accounts:index')