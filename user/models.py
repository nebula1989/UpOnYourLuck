from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_url = models.URLField(max_length=200)  # can't figure out how to get the recently created username to create a user profile url field
    life_story = models.TextField(max_length=500, default="Enter your life story here:")
    profile_img = models.ImageField(upload_to='profile_img')

    class Meta:
        db_table = 'Profile'
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return str(self.user.username)


# create a user profile automatically upon account creation using signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, profile_url=f'profile/{instance.username}')
