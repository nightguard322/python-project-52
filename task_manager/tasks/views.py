from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from task_manager.tasks.models import Status, Task
from task_manager.tasks.forms import (
    StatusModelForm,
    TaskModelForm,
    TaskFilterForm
)
from django.db.models.deletion import ProtectedError
from django.db.models import Count, Q


# Create your views here.
class StatusListView(ListView):
    model = Status
    template_name = 'status_templates/index.html'
    context_object_name = 'statuses'


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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(
                request, 
                'Невозможно удалить статус, потому что он используется'
            )
            return redirect('tasks:status_index')
        messages.success(request, 'Статус успешно удален')
        return redirect(self.success_url)


class TaskListView(ListView):
    model = Task
    template_name = 'task_templates/index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['status']:
                queryset = queryset.filter(
                    status=form.cleaned_data['status']
                )
            
            if form.cleaned_data['executor']:
                queryset = queryset.filter(
                    executor=form.cleaned_data['executor']
                )

            if form.cleaned_data['self_task']:
                queryset = queryset.filter(
                    author=self.request.user
                )

            choosed_labels = form.cleaned_data.get('labels')
            if choosed_labels:
                queryset = queryset.filter(
                    labels__label_id__in=choosed_labels
                )
                
                queryset = queryset.annotate(
                    count_labels=Count('labels', filter=Q(
                        labels__label_id__in=choosed_labels
                    ))
                ).filter(
                    count_labels=len(choosed_labels) 
                )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET)
        return context


class TaskBaseView():
    model = Task
    form_class = TaskModelForm
    template_name = 'task_templates/task_form.html'
    success_url = reverse_lazy('tasks:task_index')
    success_message = None

    def get_success_url(self):
        response = super().get_success_url()
        messages.success(self.request, self.success_message)
        return response


class TaskCreateView(LoginRequiredMixin, TaskBaseView, CreateView):
    success_message = 'Задача успешно создана'
        
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, TaskBaseView, UpdateView):
    success_message = 'Задача успешно изменена'

 
class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_templates/show.html'
    context_object_name = 'task'


class TaskDeleteView(UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'task_templates/delete.html'
    success_url = reverse_lazy('tasks:task_index')

    def get_success_url(self):
        messages.success(
            self.request,
            'Задача успешно удалена'
        )
        return super().get_success_url()

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(
                self.request, 
                'Задачу может удалить только ее автор'
            )
            return redirect(self.success_url)
        messages.errors(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        return super().handle_no_permission()
