# Generated by Django 3.2.22 on 2024-02-01 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0028_shot2_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shot2',
            name='department',
        ),
    ]
