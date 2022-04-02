# Generated by Django 4.0.2 on 2022-03-26 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stickers', '0003_alter_sticker_full_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sticker',
            options={'verbose_name': 'Sticker_Shipment', 'verbose_name_plural': 'Sticker_Shipments'},
        ),
        migrations.AlterField(
            model_name='sticker',
            name='full_name',
            field=models.CharField(default='FirstName LastName', max_length=50),
        ),
        migrations.AlterModelTable(
            name='sticker',
            table='Sticker_Shipment',
        ),
    ]