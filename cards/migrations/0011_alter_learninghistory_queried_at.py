# Generated by Django 5.0.6 on 2024-05-26 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0010_learninghistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learninghistory',
            name='queried_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
