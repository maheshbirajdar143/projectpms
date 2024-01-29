# Generated by Django 3.2.22 on 2024-01-04 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_adminextra'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='version',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='studentextra',
            name='reporting',
            field=models.CharField(choices=[('Mr. Riaz Patel (VFX Head)', 'Mr. Riaz Patel (VFX Head)'), ('Mr. Abhishek Kulkarni (Production Manager)', 'Mr. Abhishek Kulkarni (Production Manager)'), ('Mr. Swapnil Kharche (VFX Producer)', 'Mr. Swapnil Kharche (VFX Producer)'), ('Mr. Kunal Salunkhe', 'Mr. Kunal Salunkhe'), ('Mr. Ranjan Sharma', 'Mr. Ranjan Sharma'), ('Mr. Swapnil Zambare', 'Mr. Swapnil Zambare'), ('Mr. Chinmay Deshpande', 'Mr. Chinmay Deshpande'), ('Mr. Akshay Yadav', 'Mr. Akshay Yadav')], max_length=100),
        ),
    ]
