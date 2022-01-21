from django.forms import ModelForm
from registration.models import Person


class RegisterForm(ModelForm):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'email', 'phone_number')
