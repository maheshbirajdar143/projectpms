# Generated by Django 3.2.22 on 2024-01-31 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_alter_shotdepnote_recdates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuedshot',
            name='shot_version',
            field=models.CharField(blank=True, default='V000', max_length=255, null=True, verbose_name='Version No.'),
        ),
        migrations.AlterField(
            model_name='shot2',
            name='shot_version',
            field=models.CharField(blank=True, default='V000', max_length=5, null=True, verbose_name='Version No.'),
        ),
    ]
