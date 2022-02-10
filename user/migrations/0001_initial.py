# Generated by Django 4.0.1 on 2022-02-06 00:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_url', models.URLField()),
                ('life_story', models.TextField(max_length=500)),
                ('profile_img', models.ImageField(default='profile_img/default.jpg', upload_to='profile_img')),
                ('qr_code_img', models.FilePathField(path='media/qr_code/')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
                'db_table': 'Profile',
            },
        ),
    ]