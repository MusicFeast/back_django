# Generated by Django 4.0.4 on 2023-06-07 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0048_address_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderredeem',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
