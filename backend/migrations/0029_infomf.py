# Generated by Django 4.0.4 on 2022-12-08 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0028_rename_media_nftmedia_audio_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='infoMF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_community', models.TextField(blank=True, null=True)),
                ('instagram_icon', models.CharField(blank=True, default='mdi-instagram', max_length=255, null=True)),
                ('instagram_link', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter_icon', models.CharField(blank=True, default='mdi-twitter', max_length=255, null=True)),
                ('twitter_link', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook_icon', models.CharField(blank=True, default='mdi-facebook', max_length=255, null=True)),
                ('facebook_link', models.CharField(blank=True, max_length=255, null=True)),
                ('discord_icon', models.CharField(blank=True, default='discord', max_length=255, null=True)),
                ('discord_link', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
