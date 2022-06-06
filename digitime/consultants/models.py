from django.db import models


# Create your models here.
class Consultant(models.Model):
    email = models.CharField(max_length=255, null=False, blank=False)
    can_login = models.IntegerField(default=1)
    login_success_msg = models.CharField(max_length=255, blank=True, null=True)
    login_failure_msg = models.CharField(max_length=255, blank=True, null=True)


class LogEvent(models.Model):
    log_datetime = models.DateTimeField()
    token = models.CharField(max_length=1000)
    email = models.CharField(max_length=255)
    event_type = models.CharField(max_length=100)
    log_event_descr = models.CharField(max_length=1000)
