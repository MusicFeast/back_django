# Generated by Django 4.0.4 on 2023-03-20 15:03

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0040_alter_artist_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
