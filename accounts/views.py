from django.shortcuts import render
from . forms import CustomUserCreationForm, UserUpdateForm
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
    success_url = reverse_lazy('login')

class UserListView(ListView):
    model = get_user_model()
    template_name = 'user_list.html'
    context_object_name = 'users'
    success_url = reverse_lazy('accounts:index')

class UserUpdateView(UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'user_edit.html'
    context_object_name = 'user'
    success_url = reverse_lazy('accounts:index')

class UserDeleteView(DeleteView):
    model = get_user_model()
    template_name = 'confirm_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('accounts:index')

