# Generated by Django 4.0.2 on 2022-03-26 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stickers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sticker',
            name='full_name',
            field=models.CharField(default='<django.db.models.query_utils.DeferredAttribute object at 0x7fee69684850> <django.db.models.query_utils.DeferredAttribute object at 0x7fee696846a0>', max_length=50),
        ),
    ]