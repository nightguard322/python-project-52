from django.contrib.auth.views import LoginView
from .forms import CrispyLoginForm

class CrispyLoginView(LoginView):
    form_class = CrispyLoginForm
    template_name = 'registration/login.html'