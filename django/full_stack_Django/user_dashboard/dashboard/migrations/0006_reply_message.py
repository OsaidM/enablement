# Generated by Django 2.2.4 on 2022-06-22 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_remove_reply_wall'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_replys', to='dashboard.Message'),
        ),
    ]
