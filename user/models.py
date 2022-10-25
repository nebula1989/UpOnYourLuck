from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from localflavor.us.models import USStateField
from PIL import Image
import os
from platform import system as local_os
from django.utils.deconstruct import deconstructible
from django.core.files.storage import FileSystemStorage


@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, user, path):
        self.sub_path = path
        self.user = user

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}.{}'.format(instance.user.username, ext)

        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # If the filename already exists, remove it as if it was a true file system
        ext_list = ['.jpg', '.png', '.gif', '.jpeg']
        file = name.split('.')[0]

        if local_os() == 'Windows':
            file = file.split('\\')[1]
        elif local_os() == 'Linux' or local_os() == 'Darwin':
            file = file.split('/')[1]

        # Checks for other file extensions to remove
        for ext in ext_list:
            filename = 'profile_img/{}{}'.format(file, ext)
            if self.exists(filename) and file != 'default':
                os.remove(os.path.join('media', filename))
        return name


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_url = models.CharField(max_length=200)
    life_story = models.TextField(max_length=500)
    profile_img = models.ImageField(
        upload_to=UploadToPathAndRename(user, "profile_img/"),
        storage=OverwriteStorage(),
        default='profile_img/default.jpg',
    )
    qr_code_img = models.FilePathField(path='media/qr_code/')
    cashapp_link_url = models.URLField(max_length=200, default="https://cash.app/$")
    venmo_link_url = models.URLField(max_length=200, default="https://venmo.com/")
    city = models.CharField(default="Raleigh", max_length=60)
    state = USStateField(default="NC", blank=True)
    qr_scan_count = models.IntegerField(default=0)
    two_factor_enabled = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=25, default="0")
    visitor_id = models.CharField(default='0', max_length=200)
    accepted_terms_and_conditions = models.BooleanField(default=True)

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
        # set default values
        Profile.objects.create(
            user=instance, profile_url=instance.username,
        )
