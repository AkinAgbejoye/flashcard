# Generated by Django 5.0.6 on 2024-05-26 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_deck'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='deck',
            field=models.CharField(default='General', max_length=100),
        ),
    ]
