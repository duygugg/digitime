from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('email', 'can_login', 'login_success_msg', 'login_failure_msg')
    search_fields = ('email', 'id')

    fieldsets = (
        (None, {'fields': ('email', 'can_login',)}),
        ('Login Status', {'fields': ('login_success_msg', 'login_failure_msg')})
    )


admin.site.register(models.LogEvent)
