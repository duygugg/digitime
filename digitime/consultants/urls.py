from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import CanLogin

app_name = 'consultants'

urlpatterns = [
    path('canlogin/', CanLogin.as_view(), name="can-login")

]
