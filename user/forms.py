from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'form-control form-control-lg form-rounded',
                                     'placeholder': 'Email',
                                     'style': 'background-color: #3b3b3b; color: #CDD1CC;'
                                 }))
    password1 = forms.CharField(required=True,
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control form-control-lg form-rounded',
                                        'placeholder': 'Password',
                                        'style': 'background-color: #3b3b3b; color: #CDD1CC;'
                                    }))
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control form-control-lg form-rounded',
                                        'placeholder': 'Repeat Password',
                                        'style': 'background-color: #3b3b3b; color: #CDD1CC;'
                                    }))
    username = UsernameField(required=True,
                             widget=forms.TextInput(
                                 attrs={
                                     'autofocus': True,
                                     'class': 'form-control form-control-lg form-rounded', 'placeholder': 'Username',
                                     'style': 'background-color: #3b3b3b; color: #CDD1CC;'
                                 }))
    first_name = forms.CharField(required=True,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control form-control-lg form-rounded',
                                         'placeholder': 'First Name',
                                         'style': 'background-color: #3b3b3b; color: #CDD1CC;'
                                     }))
    last_name = forms.CharField(required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control form-control-lg form-rounded',
                                        'placeholder': 'First Name',
                                        'style': 'background-color: #3b3b3b; color: #CDD1CC;'
                                    }))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        widgets = {
            # 'username': forms.TextInput(attrs={'class': 'form-control form-control-lg form-rounded', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control form-control-lg form-rounded', 'placeholder': 'First Name'}),
        }

    # when save is clicked, the email input needs to be validated before saving to DB
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit and len(User.objects.filter(email=user.email)) == 0:
            user.save()
            return user
        return None


class LoginForm(AuthenticationForm):
    username = UsernameField(required=True,
                             widget=forms.TextInput(
                                 attrs={
                                     'autofocus': True,
                                     'class': 'form-control form-control-lg form-rounded',
                                     'placeholder': 'Username',
                                     'style': 'background-color: #3b3b3b; color: #CDD1CC;'
                                 }))
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'form-control form-control-lg form-rounded',
                                       'placeholder': 'Password',
                                       'style': 'background-color: #3b3b3b; color: #CDD1CC;'
                                   }))

    class Meta:
        model = User
        fields = ("username", "password")


class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(required=True,
                                   widget=forms.PasswordInput(
                                       attrs={
                                           'class': 'form-control form-control-lg form-rounded',
                                           'placeholder': 'Password',
                                           'style': 'background-color: #3b3b3b; color: #CDD1CC; border-color: transparent;'
                                       }))
    new_password1 = forms.CharField(required=True,
                                    widget=forms.PasswordInput(
                                        attrs={
                                            'class': 'form-control form-control-lg form-rounded',
                                            'placeholder': 'New Password',
                                            'style': 'background-color: #3b3b3b; color: #CDD1CC; border-color: transparent;'
                                        }))
    new_password2 = forms.CharField(required=True,
                                    widget=forms.PasswordInput(
                                        attrs={
                                            'class': 'form-control form-control-lg form-rounded',
                                            'placeholder': 'Repeat New Password',
                                            'style': 'background-color: #3b3b3b; color: #CDD1CC; border-color: transparent;'
                                        }))

    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'form-control form-control-lg form-rounded',
                                     'placeholder': 'name@example.com',
                                 }))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control form-control-lg form-rounded', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control form-control-lg form-rounded', 'placeholder': 'Last Name'}),
        }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # the other field "profile_url" must not be altered so need to specify which fields to update
        fields = ("city", "state", "profile_img", "life_story", "cashapp_link_url", "venmo_link_url")
        widgets = {
            'cashapp_link_url': forms.URLInput(attrs={'placeholder': 'https://cash.app/$yourcashtag'}),
            'venmo_link_url': forms.URLInput(attrs={'placeholder': 'https://venmo.com/$yourvenmotag'}),
        }


class UpdateTwoFactor(forms.ModelForm):
    CHOICES = [('0', 'Off'),
               ('1', 'On')]

    two_factor_enabled = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Profile
        fields = ('two_factor_enabled', 'phone_number')
