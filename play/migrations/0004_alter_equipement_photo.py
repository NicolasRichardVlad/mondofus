# Generated by Django 5.1.3 on 2024-11-24 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0003_alter_character_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipement',
            name='photo',
            field=models.ImageField(max_length=200, upload_to=''),
        ),
    ]