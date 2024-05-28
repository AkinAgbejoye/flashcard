# Generated by Django 5.0.6 on 2024-05-26 18:49

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0009_alter_card_answer_alter_card_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('queried_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('known', models.BooleanField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.card')),
            ],
        ),
    ]
