from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зарегистрировать', css_class='btn btn-primary'))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username')

        error_messages = {
            'username': {
                'required': _('Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'),
            },
            'password1': {
                'required': _('Ваш пароль должен содержать как минимум 3 символа.')
            },
            'password2': {
                'required': _('Для подтверждения введите, пожалуйста, пароль ещё раз.')
            }
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')