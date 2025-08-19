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

# Create your views here.
class StatusListView(ListView):
    model = Status
    template_name = 'status_templates/index.html'
    context_object_name = 'statuses'


class TaskListView(ListView):
    model = Task
    template_name = 'task_templates/index.html'
    context_object_name = 'tasks'


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusModelForm
    template_name = 'status_templates/status_form.html'
    success_url = reverse_lazy('statuses:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        message.success(self.request, 'Статус успешно создан')
        return response


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusModelForm
    template_name = 'status_templates/status_form.html'
    success_url = reverse_lazy('statuses:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        message.success(self.request, 'Статус успешно изменен')
        return response
    

class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'status_templates/delete.html'
    success_url = reverse_lazy('tasks:status_index')

    def delete(self, request, *args, **kwargs):
        try:
            message.success(self.request, 'Статус успешно удален')
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            message.error(self.request, 'Невозможно удалить статус, потому что он используется')
            return redirect(self.success_url)

class TaskCreateView(CreateView):
    form_class = TaskModelForm
    template_name = 'status_templates/status_form.html'
    success_url = reverse_lazy('statuses:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        message.success(self.request, 'Статус успешно создан')
        return response


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TaskModelForm
    template_name = 'status_templates/status_form.html'
    success_url = reverse_lazy('statuses:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        message.success(self.request, 'Статус успешно изменен')
        return response
    

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'status_templates/delete.html'
    success_url = reverse_lazy('statuses:index')

    def delete(self, request, *args, **kwargs):
        try:
            message.success(self.request, 'Статус успешно удален')
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            message.error(self.request, 'Невозможно удалить статус, потому что он используется')
            return redirect(self.success_url)

