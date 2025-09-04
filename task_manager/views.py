from django.contrib.auth.views import LoginView, LogoutView
from .forms import CrispyLoginForm
from django.urls import reverse_lazy
from django.contrib import messages

class CrispyLoginView(LoginView):
    form_class = CrispyLoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы залогинены')
        return response

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)