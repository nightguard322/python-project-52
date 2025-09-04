from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.tasks.models import Status, Task
from task_manager.labels.models import Label, TaggedItem
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
# Форма для создания задачи 
class TaskModelForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
        )
    
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].widget.attrs.update({
            'id': 'id_executor'
        })
        
    def save(self, commit=True):
        task = super().save(commit=False)

        if commit:
            task.save()
            task.labels.clear()
            for label in self.cleaned_data['labels']:
                TaggedItem.objects.create(
                    label=label,
                    content_object=task
                )
        return task


# Форма для фильтрации задач

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
    self_task = forms.BooleanField(
        required=False,
        label='Только свои задачи'
    )   
    labels = forms.TypedMultipleChoiceField(
        choices=[],
        coerce=int,
        required=False,
        label="Метки"
    )

    class Meta:
        fields = [
            'status', 'executor', 'self_task'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['labels'].choices = [(label.id, label.name) for label in Label.objects.all()]
