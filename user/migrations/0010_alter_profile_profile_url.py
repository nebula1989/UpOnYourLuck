# Generated by Django 4.0.2 on 2022-10-25 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_profile_profile_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_url',
            field=models.URLField(),
        ),
    ]
