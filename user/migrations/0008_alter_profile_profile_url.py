# Generated by Django 4.0.2 on 2022-10-25 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_rename_payment_link_url_profile_cashapp_link_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_url',
            field=models.TextField(max_length=200),
        ),
    ]
