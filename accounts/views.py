from django.shortcuts import render
from . forms import CustomUserCreationForm, UserChangeForm
from django.contrib.auth.forms import UserChangeForm
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.contrib.auth import get_user_model

# Create your views here.
class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = '/'

class UserListView(ListView):
    model = get_user_model()
    template_name = 'user_list.html'
    context_object_name = 'users'

class UserUpdateView(ListView):
    form_class = UserChangeForm
    template_name = 'user_edit.html'
    context_object_name = 'users'

class UserDeleteView(ListView):
    model = get_user_model()
    template_name = 'user_list.html'
    context_object_name = 'users'
