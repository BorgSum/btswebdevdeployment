from django.db import models

from django.contrib.auth.models import User

# Create your models here.

# this will be used to categorise badges
class Subject(models.Model):
	subject_id = models.BigAutoField(primary_key=True)
	subject_name = models.TextField(max_length=150)


class Report(models.Model):
	report_id = models.BigAutoField(primary_key=True)
	report_title = models.TextField(max_length=100)
	student_id = models.ForeignKey(User, on_delete=models.CASCADE)
	report_active = models.BooleanField(default=False)
	report_additional_comment = models.TextField(max_length=1000, null=True, blank=True)
	report_start_date = models.DateField()
	report_end_date = models.DateField()

class GeneratedReport(models.Model):
	gen_report_id = models.BigAutoField(primary_key=True)
	gen_report_start_date = models.DateField()
	gen_report_end_date = models.DateField()
	gen_student_id = models.ForeignKey(User, on_delete=models.CASCADE)
	gen_report_file = models.TextField(max_length=200)

