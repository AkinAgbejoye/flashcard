# Generated by Django 5.0.6 on 2024-05-28 14:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0012_alter_learninghistory_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='deck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.deck'),
        ),
    ]
