import datetime
from datetime import timedelta, date, timezone
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProjectSerializer, TaskSerializer, ConsultantSubTaskSerializer, TimeSheetSerializer, \
    SubTaskSerializer, LeaveTimeSerializer
from rest_framework import generics, status, serializers
from .models import Projects, Task, SubTask, ConsultantSubtask, TimeSheet, LeaveTime, TimesheetListObject
from consultants.models import Consultant
import json
# import library
from django.db import connection


# Create your views here.

class Index(GenericAPIView):

    def get(self, request):
        return Response(
            {' Welcome ! Here are the urls that you can navigate through: ', 'api/', 'consultants/', 'admin/'})


class ListProject(generics.ListAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer


class CreateProject(generics.CreateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer


class UpdateProject(generics.UpdateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer


class DeleteProject(generics.DestroyAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer


class ListTask(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ListConsultantSubTasks(GenericAPIView):
    print("here!!")

    def get(self, request):
        user_email = request.GET.get("email")
        consultant = Consultant.objects.filter(email=user_email)
        print("email:", user_email)
        # return Response({"data": "ok"})

        if consultant.exists():
            consultant_object = consultant[0]
            consultant_subtask_object = ConsultantSubtask.objects.filter(consultant=consultant_object)
            if consultant_subtask_object.exists():

                subtasks_data = [{
                    "consultant_subtaskID": item.id,
                    "consultant": item.consultant.email,
                    "can_login": item.consultant.can_login,
                    "projectID": item.subtask.task.project.id,
                    "project": item.subtask.task.project.title,
                    "taskID": item.subtask.task.id,
                    "task": item.subtask.task.name,
                    "subtaskID": item.subtask.id,
                    "subtask": item.subtask.name,

                } for item in consultant_subtask_object]
                print(subtasks_data)
                return Response({"data": subtasks_data})

            else:
                return Response({"data": "No subtask is assigned to this consultant"})

        else:
            return Response({"data": "No user exists with this email address"})


class ListSubtasks(generics.ListAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class ListTimeSheet(GenericAPIView):

    def get(self, request):
        # Create the cursor
        cursor = connection.cursor()

        # Write the SQL code
        sql_string = 'SELECT * FROM getList'

        # Execute the SQL
        cursor.execute(sql_string)
        result = cursor.fetchall()

        consultant_email = self.request.GET.get('email')

        consultant = Consultant.objects.filter(email=consultant_email)

        if consultant.exists():
            print(consultant)
            consultant_id = consultant[0].id

            timesheet = [x for x in result if x[0] == consultant_id]
            print(len(timesheet), ",", len([x for x in result if x[1] == 1]))

            list = [
                {
                    "id":id,
                    "consultant_id": x[0],
                    "subtask_id": x[1],
                    "date": x[4],
                    "hour": x[5],
                    "permission": x[6]
                } for id,x in enumerate(timesheet)
            ]

            return Response({"data": list, "status": 200})

        else:

            return Response({"data": "No timesheet value is entered for the consultant", "status": 404})


class CreateConsultantSubTask(generics.ListCreateAPIView):
    queryset = ConsultantSubtask.objects.all()
    serializer_class = ConsultantSubTaskSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            consultant = serializer.validated_data["consultant"]
            sub_task = serializer.validated_data["subtask"]
            # START DATE FIELD WOULD BE ASSIGNED AS TODAY'S DATA AS DEFAULT TO PREVENT KEY ERROR
            start_date = serializer.validated_data.get("start_date", date.today())
            # SAME IT GOES FOR END DATE, TAKEN AS TOMORROW'S DATE AS DEFAULT
            end_date = serializer.validated_data.get("end_date", date.today())

            if SubTask.objects.filter(id=sub_task.id).exists():
                if Consultant.objects.filter(id=consultant.id).exists():
                    if start_date <= end_date:
                        for instance in ConsultantSubtask.objects.all():
                            if instance.subtask.id == sub_task.id and instance.consultant == consultant.id:
                                raise serializers.ValidationError(
                                    "Same subtask is already assigned to a same consultant")
                            else:
                                serializer.save()

                    else:
                        raise serializers.ValidationError(
                            "Subtask must have a valid end_date value which should occur "
                            "anytime after start_date takes place")

                else:
                    raise serializers.ValidationError('There is no consultant with such id is assigned to any subtask'
                                                      )
            else:
                raise serializers.ValidationError('No sub task with such id exists')


class ListLeaveTime(generics.ListAPIView):
    queryset = LeaveTime.objects.all()
    serializer_class = LeaveTimeSerializer

    # for e in queryset:
    #     print(e.get_permissions_display(),e)
    def get(self, serializer):
        queryset = LeaveTime.objects.all()
        return Response({"data": [{"value": e.id, "label": e.get_permissions_display()} for e in queryset]})


class CreateTimeSheet(generics.ListCreateAPIView):
    queryset = TimeSheet.objects.all()
    serializer_class = TimeSheetSerializer

    def perform_create(self, serializer):
        print("backend view is active")
        if not ConsultantSubtask.objects.all():
            raise serializers.ValidationError('There is no consultant that is assigned to any subtask')

        elif not LeaveTime.objects.all():
            raise serializers.ValidationError('There is no leave time options available')

        else:
            print("data:", serializer)
            if serializer.is_valid():
                consultant_subtask = serializer.validated_data["consultant_subtask"]
                work_hour_data = serializer.validated_data["work_hour"]
                calendar = serializer.validated_data["calendar"]
                leavetime = serializer.validated_data["leave_time"]
                print("received data:", consultant_subtask, work_hour_data, calendar, leavetime)

                if ConsultantSubtask.objects.filter(id=consultant_subtask.id).exists():
                    print("consultant exists")
                    if not isinstance(work_hour_data, float):
                        raise serializers.ValidationError('Work hours must be entered in a x.xx format')
                    else:
                        # print("for loop starts")
                        # for instance in TimeSheet.objects.all():
                        #     if instance.calendar == calendar:
                        #         sum_work_hours = TimeSheet.objects.aggregate(Sum('work_hour'))
                        #         print(sum_work_hours [ "work_hour__sum" ])
                        #         if sum_work_hours [ "work_hour__sum" ] + work_hour_data > 8.00:
                        #
                        #             raise serializers.ValidationError(
                        #                 "There's already a subtask exists on timesheet that corresponds "
                        #                 "into a full day of work.Please move onto next date!!")
                        #         else:
                        print("serializer saved:")
                        serializer.save()
                        print("success")
                        return Response(data={'message': 'Succes', }, status=200)
                    # else:
                    # if work_hour_data <= 0.00 or work_hour_data > 8.00:
                    #     raise serializers.ValidationError(
                    #         'Work hours must take some value between 1 to 8 hour')
                    # else:
                    # print("success two")
                    # serializer.save(data=serializer.data)
                    # return Response(data={'message': 'Succes'}, status=200)

                else:
                    raise serializers.ValidationError(
                        'There is no such subtask exists which is assigned to this consultant')
            else:
                raise serializers.ValidationError(
                    'Serializer error')
