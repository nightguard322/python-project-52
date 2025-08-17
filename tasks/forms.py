from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Status, Task

class StatusModelForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name']

class TaskCreationForm(ModelForm):
    class Meta:
        model = Status
        fields = [__all__]