from django.shortcuts import render
from entry.models import Entry
from comment.models import Comment
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.decorators import login_required
from login.decorators import allowed_users, active_report
from report.models import Report
from django.http import HttpResponseRedirect
from badge.models import Badge, Allocation
from bts_user.models import Profile


#-------------------------------------------------------------------------------------------------------------------#
#                                              TEACHER FUNCTIONS                                                    #
#-------------------------------------------------------------------------------------------------------------------#
	
@login_required(login_url="/")
@allowed_users(allowed_roles=['staff'])
@active_report()
def teacher_dashboard_view(request, *args, **kwargs):
	user_list = User.objects.filter(groups__name='student')
	student_entries = Entry.objects.annotate(num_comments=models.Count('comment')).all().order_by('-entry_date')
	profile_list = []
	for student in user_list:
		try:
			student_profile = Profile.objects.get(user=student)
			profile_dict = {
				'user_details': student,
				'profile_details': student_profile
			}
			profile_list.append(profile_dict)
		except:
			profile_dict = {
				'user_details': student,
				'profile_details': None
			}
			profile_list.append(profile_dict)
	print(profile_list)
	content = {
		'profile_list': profile_list,
		'entry_list': student_entries,
		'student_list': user_list
	}
	return render(request, 'teacher_dashboard.html', content)



#-------------------------------------------------------------------------------------------------------------------#
#                                              STUDENT FUNCTIONS                                                    #
#-------------------------------------------------------------------------------------------------------------------#

@login_required(login_url="/")
@allowed_users(allowed_roles=['student'])
@active_report()
def student_dashboard_view(request, *args, **kwargs):
	user = request.user.id
	user_report = None
	try:
		user_report = Report.objects.get(student_id=user, report_active=True)
	except Report.DoesNotExist:
		return HttpResponseRedirect("/report")
	report = Report.objects.get(student_id=user, report_active=True)
	student_entries = Entry.objects.annotate(num_comments=models.Count('comment')).filter(report_id=user_report).order_by('-entry_date')
	alloc_list = Allocation.objects.filter(student_id=user)
	content = {
			'query_set': student_entries,
			'alloc_list': alloc_list
	}
	return render(request, 'student_dashboard.html', content)



@login_required(login_url="/")
@allowed_users(allowed_roles=['student'])
@active_report()
def student_profile_view(request, *args, **kwargs):
	valid_file_formats = ('.jpg','.jpeg','.png')
	user=request.user
	student_profile=Profile.objects.get(user=user)
	content={
		"student_profile":student_profile
	}
	if request.method == "POST":
		image = request.FILES.getlist('images')
		print("hello")
		if str(image[0]).endswith(valid_file_formats):
			print("hello")
			student_profile.image = image[0]
			student_profile.save()
	return render(request, 'student_user_profile.html', content)