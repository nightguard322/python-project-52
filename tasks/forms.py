from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Status, Task
from django.contrib.auth import get_user_model

User = get_user_model()

class StatusModelForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            })
        }

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'assignee']


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset= Status.objects.all(),
        required=False,
        label='Статус'
    )
    assignee = forms.ModelChoiceField(
        queryset= User.objects.all(),
        required=False,
        label='Исполнитель'
    )
    self_task = forms.