from django.shortcuts import render
from datetime import timedelta, date, timezone
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ConsultantSerializer
from rest_framework import generics, status, serializers
from .models import Consultant
import json


# Create your views here.

class CanLogin(GenericAPIView):

    def get(self, request):
        consultant_email = request.GET.get("email")
        consultant_object = Consultant.objects.filter(email=consultant_email)

        if consultant_object.exists():
            consultant_object = consultant_object [ 0 ]
            can_login = consultant_object.can_login
            if can_login == 1:
                data = [ {
                    "id": consultant_object.id,
                    "login_msg": consultant_object.login_success_msg,
                    "email": consultant_object.email,
                    "status": 200
                } ]

                return Response({"data": data, "status": 200})
            else:
                data = [ {
                    "id": consultant_object.id,
                    "login_msg": consultant_object.login_failure_msg,
                    "email": consultant_object.email,
                    "status": 203
                } ]

                return Response({"data": data, "status": 203})
        else:
            return Response({"data": "No user exists!", "status": status.HTTP_404_NOT_FOUND})
