from django.shortcuts import render
from . forms import CustomUserCreationForm, UserChangeForm
from django.contrib.auth.forms import UserChangeForm
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

# Create your views here.
class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('users')

class UserListView(ListView):
    model = get_user_model()
    template_name = 'user_list.html'
    context_object_name = 'users'
    success_url = reverse_lazy('users:signup')

class UserUpdateView(ListView):
    form_class = UserChangeForm
    template_name = 'user_edit.html'
    context_object_name = 'users'
    success_url = reverse_lazy('users:update')

class UserDeleteView(ListView):
    model = get_user_model()
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('users')
