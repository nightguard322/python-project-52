from django import forms
from labels.models import Label

class LabelBaseForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            })
        }