from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import datetime
from report.models import Report

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				if request.user.groups.all()[0].name == 'student':
					return HttpResponseRedirect("/student/")
				elif request.user.groups.all()[0].name == 'staff':
					return HttpResponseRedirect("/teacher/")
				else:
					return HttpResponseRedirect("/")
		return wrapper_func
	return decorator

# to the active active_report run an overall check on the decorator ensure that there is an existing report
# for students and have it redirect in the same way as the inactive report. This decarator needs more checks
# to ensure more robust 

def active_report():
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if request.user.groups.all()[0].name == 'student':
				#try:
				user = User.objects.get(id=request.user.id)
				current_date = datetime.date.today()
				current_report = Report.objects.get(student_id=user, report_active=True)
				if current_date > current_report.report_start_date and current_date < current_report.report_end_date:
					return view_func(request, *args, **kwargs)
					# add a page to tell students they have no active report and to contact admin for its creation
				return HttpResponseRedirect("/no_report")
				# except:
				# 	return HttpResponseRedirect("/no_report")
			return view_func(request, *args, **kwargs)
		return wrapper_func
	return decorator