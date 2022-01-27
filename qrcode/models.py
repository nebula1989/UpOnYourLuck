from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class QRCode(models.Model):
    associated_user = models.CharField(max_length=200, default='None', primary_key=True)
    profile_url = models.URLField(max_length=200)

    class Meta:
        db_table = 'QRCode'
        verbose_name = "QRCode"
        verbose_name_plural = "QRCodes"

    def __str__(self):
        return self.associated_user

