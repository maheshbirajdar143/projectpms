# Generated by Django 3.2.22 on 2024-01-03 04:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20240103_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShotStatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_status', models.CharField(max_length=255)),
                ('change_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('shot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_history', to='user.shot2')),
            ],
        ),
        migrations.DeleteModel(
            name='InternalStatusChange',
        ),
    ]
