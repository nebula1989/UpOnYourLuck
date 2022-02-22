from django import forms
from django.contrib.auth.forms import UsernameField

from .models import Stickers


class SendStickerForm(forms.ModelForm):
    full_name = UsernameField(required=True,
                              widget=forms.TextInput(
                                  attrs={
                                      'autofocus': True,
                                      'class': 'form-control form-control-lg form-rounded',
                                      'placeholder': 'FirstName LastName'
                                  }))
    address = forms.CharField(required=True,
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'form-control form-control-lg form-rounded',
                                      'placeholder': '123 Upon Your Luck Street'
                                  }))
    city = forms.CharField(required=True,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control form-control-lg form-rounded',
                                   'placeholder': 'Raleigh'
                               }))
    state = forms.CharField(required=True,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control form-control-lg form-rounded',
                                    'placeholder': 'NC'
                                }))
    zip_code = forms.CharField(required=True,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control form-control-lg form-rounded',
                                   'placeholder': '90210'
                               }))

    class Meta:
        model = Stickers
        fields = '__all__'
