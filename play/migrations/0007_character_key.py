# Generated by Django 5.1.3 on 2024-11-24 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0006_character_puissance'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='key',
            field=models.BooleanField(default=False),
        ),
    ]
