from django.contrib import admin

from .models import Report, Subject, GeneratedReport
# Register your models here.
admin.site.register(Subject)
admin.site.register(Report)
admin.site.register(GeneratedReport)

