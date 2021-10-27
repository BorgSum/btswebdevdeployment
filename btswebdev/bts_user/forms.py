from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Staff, Student


class UserLoginForm(UserCreationForm):
	# add overides to the form field here
	class Meta:
		model = Student
		fields = [
			# add all student fields here later
		]


# 