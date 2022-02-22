# Generated by Django 4.0.2 on 2022-02-22 02:17

from django.db import migrations, models
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('stickers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stickers',
            name='city',
            field=models.CharField(default='Raleigh', max_length=100),
        ),
        migrations.AlterField(
            model_name='stickers',
            name='full_name',
            field=models.CharField(default='FirstName LastName', max_length=50),
        ),
        migrations.AlterField(
            model_name='stickers',
            name='ship_to_address',
            field=models.CharField(default='123 Street St', max_length=50),
        ),
        migrations.AlterField(
            model_name='stickers',
            name='state',
            field=localflavor.us.models.USStateField(default='NC', max_length=2),
        ),
    ]
