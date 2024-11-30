# Generated by Django 5.1.3 on 2024-11-26 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_company_current_employee_estimate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='uuid',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]