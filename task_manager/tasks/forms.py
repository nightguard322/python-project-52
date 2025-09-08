from django import forms
from task_manager.tasks.models import Status, Task
from task_manager.labels.models import Label, TaggedItem
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

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
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control'}
        ),
        label='Метки'
        )
    
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor']
        widgets = {
            'executor': forms.Select(attrs={
                'aria-label': "Исполнитель",
                'class': 'form-select',
            }),
        }

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].label_from_instance = (
            lambda user: f"{user.first_name} {user.last_name}"
        )
        if self.instance and self.instance.pk:
            selected_labels_ids = TaggedItem.objects.filter(
                content_type=ContentType.objects.get_for_model(Task),
                object_id=self.instance.pk
            ).values_list('label_id', flat=True)
            self.fields['labels'].initial = Label.objects.filter(
                id__in=selected_labels_ids
            )

# Форма для фильтрации задач


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label='Статус'
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
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
        label="Метка"
    )

    class Meta:
        fields = [
            'status', 'executor', 'self_task'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['labels'].choices = [
            (label.id, label.name)
            for label
            in Label.objects.all()
        ]
        self.fields['executor'].label_from_instance = (
            lambda user: f"{user.first_name} {user.last_name}"
        )