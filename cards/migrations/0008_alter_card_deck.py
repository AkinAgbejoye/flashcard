# Generated by Django 5.0.6 on 2024-05-26 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_alter_card_deck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='deck',
            field=models.CharField(choices=[('Pyhsics', 'Pyhsics'), ('Cryptocurrency', 'Cryptocurrency')], default='General', max_length=100),
        ),
    ]
