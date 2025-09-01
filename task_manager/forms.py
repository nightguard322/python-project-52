from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django.contrib.auth.forms import AuthenticationForm

class CrispyLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Войти', css_class='btn btn-primary'))
