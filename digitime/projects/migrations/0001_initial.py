# Generated by Django 4.0.4 on 2022-06-01 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('consultants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultantSubtask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultants.consultant')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissions', models.CharField(choices=[('NA', 'Not Available'), ('SL', 'Sick Leave'), ('V', 'Vacation'), ('BFL', 'Breast-feeding Leave'), ('BL', 'Bereavement Leave'), ('ML', 'Maternity Leave'), ('PL', 'Paternity Leave'), ('ML', 'Marriage License'), ('CL', 'Compassionate Leave'), ('NP', 'Notice Period'), ('S', 'School'), ('NH', 'National Holiday')], default='NA', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Open', 'Open'), ('InProgress', 'In Progress'), ('Review', 'Review'), ('Ready', 'Ready'), ('Completed', 'Completed'), ('OnHold', 'On Hold')], default='Open', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendar', models.IntegerField(default=100000)),
                ('work_hour', models.FloatField(default=8.0)),
                ('consultant_subtask', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.consultantsubtask')),
                ('leave_time', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.leavetime')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=1000)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.projects')),
            ],
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=1000)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.task')),
            ],
        ),
        migrations.AddField(
            model_name='projects',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.status'),
        ),
        migrations.AddField(
            model_name='consultantsubtask',
            name='subtask',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.subtask'),
        ),
    ]