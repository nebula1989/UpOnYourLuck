from django.db import models
from localflavor.us.models import USStateField, USZipCodeField


# this data will essentially be what's on the shipping label
class StickerShipment(models.Model):
    full_name = models.CharField(max_length=50, default="")
    street_name_and_number = models.CharField(max_length=99, default="")
    state = USStateField(default="", blank=False)
    city = models.CharField(max_length=50, default="", blank=False)
    zipcode = USZipCodeField(default="", blank=False)

    class Meta:
        db_table = 'Sticker_Shipment'
        verbose_name = "Sticker_Shipment"
        verbose_name_plural = "Sticker_Shipments"

    def __str__(self):
        return self.street_name_and_number + " "
