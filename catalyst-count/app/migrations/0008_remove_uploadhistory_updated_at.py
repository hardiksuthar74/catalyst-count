# Generated by Django 5.1.3 on 2024-11-28 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_uploadhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadhistory',
            name='updated_at',
        ),
    ]