# Generated by Django 5.1.3 on 2024-11-28 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_uploadhistory_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadhistory',
            name='task',
        ),
    ]