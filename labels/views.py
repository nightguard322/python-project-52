from django.shortcuts import render
from django.views.generic import(
    ListView,
    UpdateView,
    DeleteView,
    CreateView
)
from labels.models import Label
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class LabelListView(DetailView):
    model = Label
    template_name = 'index.html'
    success_url = reverse('labels:index')

class LabelBaseView():
    model = Label
    form = LabelCreateForm
    template_name = 'label_form.html'
    success_url = reverse("labels:index")
    success_message = None

    def form_valid(self, form):
        response = super().form_valid(form)
        message.success(self.request, self.success_message)
        return response

class LabelCreateView(LoginRequiredMixin, LabelBaseView, CreateView):
    success_message = 'Метка успешно создана'

class LabelUpdateView(LoginRequiredMixin, LabelBaseView, UpdateView):
    success_message = 'Метка успешно изменена'

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'delete.html'
    success_url = reverse('labels:delete')

    def delete(self, request, *args, **kwargs):
        try:
            messages.success(self.request, 'Метка успешно удалена')
            return super().delete(self.request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, 'Невозможно удалить метку, потому что она используется')
            return redirect(self.success_url)

