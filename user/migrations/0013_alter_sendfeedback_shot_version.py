# Generated by Django 3.2.22 on 2024-01-08 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20240108_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendfeedback',
            name='shot_version',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Version No.'),
        ),
    ]
