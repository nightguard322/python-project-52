from django.shortcuts import render
from django.view.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django contrib import messages
from .models import Status, Task
from .forms import StatusModelForm, TasksCreationForm

# Create your views here.
class StatusListView(ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'


class StatusCreateView(CreateView):
    form = StatusModelForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        message.success(self.request, 'Статус успешно создан')
        return response


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    form = StatusModelForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        message.success(self.request, 'Статус успешно изменен')
        return response
    

class StatusDeleteView(LoginRequiredMixin, DeleteView):
    form = StatusModelForm
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses:index')

    def delete(self, request, *args, **kwargs):
        try:
            message.success(self.request, 'Статус успешно удален')
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            message.error(self.request, 'Невозможно удалить статус, потому что он используется')
            return redirect(self.success_url)

