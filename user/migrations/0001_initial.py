# Generated by Django 3.2.22 on 2024-01-02 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentIssuedShot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shot_name', models.CharField(max_length=255)),
                ('department', models.CharField(max_length=100)),
                ('mandays', models.PositiveIntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IssuedShot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=255)),
                ('project_name', models.CharField(max_length=255)),
                ('shot_name', models.CharField(max_length=255)),
                ('shot_version', models.IntegerField(blank=True, null=True, verbose_name='Version No.')),
                ('work_description', models.CharField(max_length=2550, verbose_name='Scope of Work')),
                ('department', models.CharField(max_length=100)),
                ('issuedate', models.DateField(blank=True, default=None, null=True)),
                ('eta', models.DateField(blank=True, default=None, null=True)),
                ('work_status', models.CharField(choices=[('YTS', 'YTS'), ('WIP', 'WIP'), ('DONE', 'DONE'), ('HOLD', 'HOLD'), ('Not Assigned', 'Not Assigned'), ('Assigned', 'Assigned')], max_length=255, verbose_name='Shot Status')),
                ('note', models.CharField(blank=True, default=None, max_length=2000, null=True)),
                ('content', models.CharField(blank=True, default=None, max_length=2000, null=True)),
                ('overdue', models.IntegerField(blank=True, default=0, null=True)),
                ('manday', models.IntegerField(blank=True, default=0, null=True)),
                ('received_date', models.DateField(blank=True, default=None, null=True)),
                ('image1', models.ImageField(blank=True, default=None, null=True, upload_to='annot_images/')),
                ('kbk_image', models.ImageField(blank=True, default=None, null=True, upload_to='kbk_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Shot2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255, verbose_name='Project Name')),
                ('shot_name', models.CharField(max_length=2040, verbose_name='Shot Name')),
                ('work_description', models.CharField(max_length=2550, verbose_name='Scope of Work')),
                ('date_started', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created (Y-M-D)')),
                ('eta', models.DateField(blank=True, default=None, null=True, verbose_name='TGT Date (y-m-d)')),
                ('dependency', models.TextField(verbose_name='Dependency')),
                ('work_status', models.CharField(choices=[('Not Assigned', 'Not Assigned'), ('Assigned', 'Assigned')], default='Not Assigned', max_length=255, verbose_name='Assignment')),
                ('final_status', models.CharField(blank=True, default='N/A', max_length=255, null=True, verbose_name='Final Status')),
                ('internal_status', models.CharField(blank=True, default='YTS', max_length=255, null=True, verbose_name='Internal Status')),
                ('remark', models.CharField(blank=True, default='N/A', max_length=1000, null=True, verbose_name='Remark')),
                ('client_status', models.CharField(blank=True, default='N/A', max_length=255, null=True, verbose_name='Client Status')),
                ('added_column', models.JSONField(blank=True, default=dict, null=True)),
                ('shot_version', models.IntegerField(blank=True, default=1, null=True, verbose_name='Version No.')),
                ('comp_status', models.CharField(choices=[('Ok', 'OK'), ('Pending', 'Pending')], default='Pending', max_length=510, verbose_name='Comp Status')),
                ('column_order', models.TextField()),
                ('issued_date', models.DateTimeField(blank=True, null=True, verbose_name='Reviewed Date')),
                ('issued_by', models.CharField(blank=True, default='N/A', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.DateTimeField(blank=True, null=True)),
                ('logout_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentExtra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aid', models.IntegerField(unique=True)),
                ('department', models.CharField(choices=[('Account', 'Account'), ('CG', 'CG'), ('Comp', 'Comp'), ('DMP', 'DMP'), ('Editor', 'Editor'), ('HR', 'HR'), ('IT', 'IT'), ('MGFX', 'MGFX'), ('Matchmove', 'Matchmove'), ('Paint', 'Paint'), ('Pipeline', 'Pipeline'), ('Production', 'Production'), ('Roto', 'Roto')], max_length=100)),
                ('designation', models.CharField(choices=[('Intern', 'Intern'), ('Trainee', 'Trainee'), ('Jr. Artist', 'Jr. Artist'), ('Sr. Artist', 'Sr. Artist'), ('TD', 'TD'), ('Data IO', 'Data IO'), ('System Admin', 'System Admin'), ('Coordinator', 'Coordinator'), ('Team Lead', 'Team Lead'), ('Supervisor', 'Supervisor'), ('Manager', 'Manager')], max_length=100)),
                ('reporting', models.CharField(choices=[('Mr. Riaz Patel', 'Mr. Riaz Patel'), ('Mr. Abhishek Kulkarni', 'Mr. Abhishek Kulkarni'), ('Mr. Swapnil Kharche', 'Mr. Swapnil Kharche'), ('Mr. Kunal Salunkhe', 'Mr. Kunal Salunkhe'), ('Mr. Swapnil Zambare', 'Mr. Swapnil Zambare'), ('Mr. Chinmay Deshpande', 'Mr. Chinmay Deshpande'), ('Mr. Akshay Yadav', 'Mr. Akshay Yadav')], max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShotHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=255)),
                ('previous_value', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('updated_value', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('shot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.shot2')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SendFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=255)),
                ('project_name', models.CharField(max_length=255)),
                ('shot_name', models.CharField(max_length=255)),
                ('department', models.CharField(max_length=255)),
                ('work_status', models.CharField(choices=[('YTS', 'YTS'), ('WIP', 'WIP'), ('DONE', 'DONE'), ('HOLD', 'HOLD'), ('Not Assigned', 'Not Assigned'), ('Assigned', 'Assigned')], max_length=255)),
                ('content', models.CharField(max_length=2000, verbose_name='Comment')),
                ('shot_version', models.IntegerField(blank=True, null=True, verbose_name='Version No.')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='annot_images/')),
                ('issued_shot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.issuedshot')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewed_date', models.DateTimeField(auto_now=True)),
                ('reviewed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.shot2')),
            ],
        ),
        migrations.CreateModel(
            name='InternalStatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_status', models.CharField(max_length=255)),
                ('date_changed', models.DateTimeField(auto_now_add=True)),
                ('shot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internal_status_history', to='user.shot2')),
            ],
        ),
        migrations.CreateModel(
            name='ArtistMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now)),
                ('shot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.shot2')),
            ],
        ),
        migrations.CreateModel(
            name='Approve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved_date', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.shot2')),
            ],
        ),
    ]
