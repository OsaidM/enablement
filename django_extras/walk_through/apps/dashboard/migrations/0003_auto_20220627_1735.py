# Generated by Django 2.2.4 on 2022-06-27 14:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20220627_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_level',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]