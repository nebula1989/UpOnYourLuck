from django.db import models
from localflavor.us.models import USStateField, USZipCodeField


# this data will essentially be what's on the shipping label
class StickerShipment(models.Model):
    full_name = models.CharField(max_length=50, default="FirstName LastName")
    street_name_and_number = models.CharField(max_length=99, default=f"100 ABC st")
    state = USStateField(default="NC", blank=False)
    city = models.CharField(max_length=50, default="Raleigh", blank=False)
    zipcode = USZipCodeField(default="27513", blank=False)

    class Meta:
        db_table = 'Sticker_Shipment'
        verbose_name = "Sticker_Shipment"
        verbose_name_plural = "Sticker_Shipments"

    def __str__(self):
        return self.full_name + "\n" +\
               self.street_name_and_number + "\n" +\
               self.city + ", " + self.state + "\n" +\
               self.zipcode
