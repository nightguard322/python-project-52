from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserUpdateForm
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

# Create your views here.
class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return response

class UserListView(ListView):
    model = get_user_model()
    template_name = 'user_list.html'
    context_object_name = 'users'
    success_url = reverse_lazy('accounts:index')

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'user_edit.html'
    context_object_name = 'user'
    success_url = reverse_lazy('accounts:index')

    def test_func(self):
        return self.request.user == self.get_object() #проверка что юзер текущий
    
    def handle_no_permission(self):     
        if self.request.user.is_authenticated:
            messages.error(self.request, 'У вас нет прав для изменения другого пользователя.')
            return redirect(reverse('accounts:index'))
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect(reverse('login'))

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Пользователь успешно изменен')
        return response

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    template_name = 'confirm_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('accounts:index')

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'У вас нет прав для изменения другого пользователя.')
            return redirect(reverse('accounts:index'))
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request, 'Невозможно удалить пользователя, потому что он используется') 
            return redirect("accounts:index")
        messages.success(request, 'Пользователь успешно удален')
        return redirect(self.success_url) 