from django.contrib.auth.models import User
from django.db import models
from localflavor.us.models import USStateField, USZipCodeField
from localflavor.us import us_states


# Create your models here.
class Stickers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=50, default='FirstName LastName')
    ship_to_address = models.CharField(max_length=50, default='123 Street St')
    city = models.CharField(max_length=100, default='Raleigh')
    state = USStateField(max_length=50, default='NC', choices=us_states.STATE_CHOICES)
    zip_code = USZipCodeField(max_length=5, default=27587)

    class Meta:
        db_table = 'Sticker'
        verbose_name = "Sticker"
        verbose_name_plural = "Stickers"
