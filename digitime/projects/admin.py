from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'description')


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'description')


@admin.register(models.SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'description')


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['status']


@admin.register(models.LeaveTime)
class LeaveTimeAdmin(admin.ModelAdmin):
    list_display = ['permissions']


@admin.register(models.ConsultantSubtask)
class ConsultantSubtaskAdmin(admin.ModelAdmin):
    list_display = ('subtask', 'consultant', 'start_date', 'end_date')
    search_fields = ('subtask', 'consultant')
    ordering = ('-start_date',)


@admin.register(models.TimeSheet)
class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ('consultant_subtask', 'calendar', 'work_hour', 'leave_time')
    search_fields = ('consultant_subtask',)
