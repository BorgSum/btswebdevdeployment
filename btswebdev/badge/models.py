from django.db import models
from report.models import Subject

from django.contrib.auth.models import User


class Badge(models.Model):
	badge_id = models.BigAutoField(primary_key=True)
	badge_title = models.TextField(max_length=200)
	badge_description = models.TextField(max_length=500)
	badge_allocated_image = models.ImageField(null=True, blank=True, upload_to="images/badges")
	badge_unallocated_image = models.ImageField(null=True, blank=True, upload_to="images/badges")
	badge_how_to_obtain = models.TextField(max_length=200, null=True, blank=True) 
	badge_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)

class Allocation(models.Model):
	allocation_id = models.BigAutoField(primary_key=True)
	student_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students_badge')
	staff_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_badge')
	badge_id = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='alloc_list')
	alloc_date = models.DateTimeField(auto_now=True)