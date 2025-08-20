from django.shortcuts import render
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Status, Task
from .forms import StatusModelForm, TaskModelForm
from django.db.models.deletion import ProtectedError

# Create your views here.

class StatusListView(ListView):
    model = Status
    template_name = 'status_templates/index.html'
    context_object_name = 'statuses'


class TaskListView(ListView):
    model = Task
    template_name = 'task_templates/index.html'
    context_object_name = 'tasks'


class StatusBaseView():
    model = Status
    form_class = StatusModelForm
    template_name = 'status_templates/status_form.html'
    success_url = reverse_lazy('tasks:status_index')
    success_message = None

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class StatusCreateView(LoginRequiredMixin, StatusBaseView, CreateView):
    success_message = 'Статус успешно создан'

class StatusUpdateView(LoginRequiredMixin, StatusBaseView, UpdateView):
    success_message = 'Статус успешно изменен'


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'status_templates/delete.html'
    success_url = reverse_lazy('tasks:status_index')

    def get_success_url(self):
        messages.success(self.request, 'Статус успешно удален')
        return self.success_url

    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, 'Невозможно удалить статус, потому что он используется')
            return self.success_url


class TaskBaseView():
    form_class = TaskModelForm
    template_name = 'task_templates/status_form.html'
    success_url = reverse_lazy('tasks:task_index')
    success_message = None

class TaskCreateView(LoginRequiredMixin, TaskBaseView, UpdateView):
    success_message = 'Задача успешно создана'

class TaskUpdateView(LoginRequiredMixin, TaskBaseView, UpdateView):
    success_message = 'Задача успешно изменена'
    

class TaskDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'status_templates/delete.html'
    success_url = reverse_lazy('statuses:index')

    def get_success_url(self):
        messages.success(self.request, 'Статус успешно удален')
        return super().get_success_url

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Задачу может удалить только ее автор')
            return success_url
        message.errors(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect(reverse('login'))

