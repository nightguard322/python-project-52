from django.shortcuts import render, redirect
from django.views.generic import(
    ListView,
    UpdateView,
    DeleteView,
    CreateView
)
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelBaseForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy


# Create your views here.
class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels_index.html'
    success_url = reverse_lazy('labels:index')
    context_object_name = 'labels'

class LabelBaseView():
    model = Label
    form_class = LabelBaseForm
    template_name = 'labels_form.html'
    success_url = reverse_lazy("labels:index")
    success_message = None

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class LabelCreateView(LoginRequiredMixin, LabelBaseView, CreateView):
    success_message = 'Метка успешно создана'

class LabelUpdateView(LoginRequiredMixin, LabelBaseView, UpdateView):
    success_message = 'Метка успешно изменена'

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels_delete.html'
    success_url = reverse_lazy('labels:index')
    context_object_name = 'label'

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(self.request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, 'Невозможно удалить метку, потому что она используется')
            return redirect(self.success_url)
        
    def get_success_url(self):
        messages.success(self.request, 'Метка успешно удалена')
        return super().get_success_url()

