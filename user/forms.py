from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True, 
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control form-control-lg form-rounded',
                'placeholder': 'Email'
            }))
    password1 = forms.CharField(required=True, 
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control form-control-lg form-rounded',
                'placeholder': 'Password'
            }))
    password2 = forms.CharField(required=True, 
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control form-control-lg form-rounded',
                'placeholder': 'Repeat Password'
            }))

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg form-rounded', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-lg form-rounded', 'placeholder': 'First Name'}),
        }

    # when save is clicked, the email input needs to be validated before saving to DB
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = UsernameField(required=True,
        widget = forms.TextInput(
            attrs = {
                'autofocus': True,
                'class': 'form-control form-control-lg form-rounded',
                'placeholder': 'Username'
            }))
    password = forms.CharField(required=True,
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control form-control-lg form-rounded',
                'placeholder': 'Password'
            }))

    class Meta:
        model = User
        fields = ("username", "password")
        


"""class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']"""


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # the other field "profile_url" must not be altered so need to specify which fields to update
        fields = ("city", "state", "profile_img", "life_story", "payment_link_url")
        widgets = {
            'payment_link_url': forms.URLInput(attrs={'placeholder': 'https://cash.app/$yourcashtag'}),
        }