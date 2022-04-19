from django import forms
from .models import StickerShipment


class ShipStickerForm(forms.ModelForm):
    class Meta:
        model = StickerShipment
        fields = '__all__'

        #fields = ['full_name', 'street_name_and_number', 'state', 'city', 'zipcode']
        """
        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-control form-rounded', 'placeholder': 'Full Name'}),
            'street_name_and_number': forms.TextInput(
                attrs={'class': 'form-control form-rounded', 'placeholder': 'Address'}),
            'state': forms.TextInput(
                attrs={'class': 'form-control form-rounded', 'placeholder': 'State'}),
            'city': forms.TextInput(
                attrs={'class': 'form-control form-rounded', 'placeholder': 'City'}),
            'zipcode': forms.TextInput(
                attrs={'class': 'form-control form-rounded', 'placeholder': 'Zip'}),
        }
        """




