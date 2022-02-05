from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_url = models.URLField(max_length=200)
    life_story = models.TextField(max_length=500)
    profile_img = models.ImageField(upload_to='profile_img', default='profile_img/default.jpg')
    qr_code_img = models.FilePathField(max_length=150)

    class Meta:
        db_table = 'Profile'
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_img.path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_img.path)

    def get_profile_url(self):
        return self.profile_url


# create a user profile automatically upon account creation using signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # set default values for profile url, and qr code img
        Profile.objects.create(
            user=instance, profile_url=f'profile/{instance.username}',
        )

