# Generated by Django 4.0.4 on 2022-10-10 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
