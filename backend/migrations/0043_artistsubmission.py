# Generated by Django 4.0.4 on 2023-03-28 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0042_artist_banner_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default='', max_length=255)),
                ('name_artist', models.CharField(default='', max_length=255)),
                ('genere', models.CharField(default='', max_length=255)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook', models.CharField(blank=True, max_length=255, null=True)),
                ('instagram', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
