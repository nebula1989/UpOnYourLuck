# Generated by Django 4.0.2 on 2022-10-25 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_profile_accepted_terms_and_conditions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='accepted_terms_and_conditions',
            field=models.BooleanField(default=True),
        ),
    ]
