# Generated by Django 4.0.4 on 2023-01-20 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0033_userroles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
