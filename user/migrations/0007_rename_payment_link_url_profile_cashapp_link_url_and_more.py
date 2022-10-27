# Generated by Django 4.0.2 on 2022-10-25 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_delete_followerscount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='payment_link_url',
            new_name='cashapp_link_url',
        ),
        migrations.AddField(
            model_name='profile',
            name='venmo_link_url',
            field=models.URLField(default='https://venmo.com/'),
        ),
    ]