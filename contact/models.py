from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    username = models.CharField(max_length=100, null=True, primary_key=False)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'Contact'
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
