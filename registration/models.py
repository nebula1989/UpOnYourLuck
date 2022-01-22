from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=50, null=True, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'."
                                         " Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    account_created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Person'
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
