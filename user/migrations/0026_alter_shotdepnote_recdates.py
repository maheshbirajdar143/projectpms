# Generated by Django 3.2.22 on 2024-01-31 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_shotdepnote_recdates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shotdepnote',
            name='recdates',
            field=models.DateField(blank=True, null=True, verbose_name='Date Received'),
        ),
    ]
