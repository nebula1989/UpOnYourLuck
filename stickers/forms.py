from django import forms
from .models import StickerShipment


class ShipStickerForm(forms.ModelForm):
    class Meta:
        model = StickerShipment
        fields = '__all__'
