from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import ListProject, CreateProject, CreateConsultantSubTask, CreateTimeSheet, ListSubtasks, ListTimeSheet, \
    ListConsultantSubTasks,ListLeaveTime

app_name = 'projects'

urlpatterns = [
    path('list/projects/', ListProject.as_view(), name='list-projects'),
    path('create-project/', CreateProject.as_view(), name='create-projects'),
    # path('create-consultant-subtask/', CreateConsultantSubTask.as_view(), name='create-consultant-subtask'),
    path('create/timesheet/', CreateTimeSheet.as_view(), name='create-timesheet'),
    path('list/subtasks/', ListSubtasks.as_view(), name="list-subtasks"),
    path('list/timesheet/', ListTimeSheet.as_view(), name="list-timesheet"),
    path("list/consultant-subtasks/", ListConsultantSubTasks.as_view(), name="list-consultant-subtask"),
    path('list/leavetime/', ListLeaveTime.as_view(), name="list-leavetime"),
]
