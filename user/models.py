from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_url = models.URLField(max_length=200, default=('profile/' + str(User.username)))
    life_story = models.TextField(max_length=500, default="My Life Story")

    class Meta:
        db_table = 'Profile'
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return str(self.user.username)

