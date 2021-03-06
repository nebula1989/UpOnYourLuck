# Generated by Django 4.0.2 on 2022-04-06 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_profile_qr_scan_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default='0', max_length=25),
        ),
        migrations.AddField(
            model_name='profile',
            name='two_factor_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='visitor_id',
            field=models.CharField(default='0', max_length=200),
        ),
    ]
