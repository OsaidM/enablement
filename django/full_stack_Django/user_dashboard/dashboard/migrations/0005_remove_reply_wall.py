# Generated by Django 2.2.4 on 2022-06-22 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20220622_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='wall',
        ),
    ]