from rest_framework import serializers
from .models import *


class StatusFormSerializer(serializers.Serializer):
    def list(self):
        projects = Projects.objects.all()
        for project in projects:
            status = project [ 'status' ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


class ConsultantSubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultantSubtask
        fields = '__all__'


class TimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet
        fields = '__all__'


class LeaveTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveTime
        fields = '__all__'
