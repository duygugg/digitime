import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from consultants.models import Consultant
from datetime import datetime, date
from dbview.models import DbView


# Create your models here.


class LeaveTime(models.Model):
    choices_permissions = [
        ('NA', 'Not Available'),
        ('SL', 'Sick Leave'),
        ('V', 'Vacation'),
        ('BFL', 'Breast-feeding Leave'),
        ('BL', 'Bereavement Leave'),
        ('ML', 'Maternity Leave'),
        ('PL', 'Paternity Leave'),
        ('ML', 'Marriage License'),
        ('CL', 'Compassionate Leave'),
        ('NP', 'Notice Period'),
        ('S', 'School'),
        ('NH', 'National Holiday')

    ]

    permissions = models.CharField(max_length=3, choices=choices_permissions, default='NA')

    permissionLabel = models.CharField( max_length=255, blank=True, null=True)

    def __str__(self):
        return self.permissions



class TimesheetListObject(models.Model):
    id = models.IntegerField(primary_key=True)
    calendardate = models.CharField(db_column='calendardate', max_length = 4000, blank = True, null = True)
    work_hour = models.FloatField(db_column='work_hour')
    permissionLabel = models.CharField(db_column='permissionLabel',max_length=255, blank=True,
                                       null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't
        db_table = 'getList'


class Status(models.Model):
    status_choices = [
        ('Open', 'Open'),
        ('InProgress', 'In Progress'),
        ('Review', 'Review'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
        ('OnHold', 'On Hold')
    ]

    status = models.CharField(max_length=20, choices=status_choices, default='Open')

    def __str__(self):
        return self.status


class Projects(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Task(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    project = models.ForeignKey(Projects, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.project.title + " " + self.name


class SubTask(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    task = models.ForeignKey(Task, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.task.project.title + " " + self.task.name + " " + self.name


class ConsultantSubtask(models.Model):
    subtask = models.ForeignKey(SubTask, on_delete=models.CASCADE)
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.id)


class TimeSheet(models.Model):
    calendar = models.IntegerField(default=100000)
    consultant_subtask = models.ForeignKey(ConsultantSubtask, blank=True, null=True, on_delete=models.SET_NULL)
    work_hour = models.FloatField(default=8.00)
    leave_time = models.ForeignKey(LeaveTime, blank=True, null=True, on_delete=models.SET_NULL)
