# Generated by Django 4.0.4 on 2023-09-13 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0052_alter_drivenft_email_alter_orderredeem_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet', models.CharField(blank=True, max_length=255, null=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('discord_id', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter', models.CharField(blank=True, max_length=255, null=True)),
                ('bio', models.CharField(blank=True, max_length=255, null=True)),
                ('track_demo', models.CharField(blank=True, max_length=255, null=True)),
                ('track_desc', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
