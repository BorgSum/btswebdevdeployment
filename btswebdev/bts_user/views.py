from django.shortcuts import render
from django.contrib.auth.models import User
from badge.models import Badge, Allocation
from entry.models import Entry
from report.models import Report
from django.db import models
from django.contrib.auth.decorators import login_required
from login.decorators import allowed_users, active_report
from django.http import HttpResponseRedirect, Http404
from bts_user.models import Profile

#-------------------------------------------------------------------------------------------------------------------#
#                                              TEACHER FUNCTIONS                                                    #
#-------------------------------------------------------------------------------------------------------------------#

# ************************************************************* #
#																#
#  	URLpattern: teacher/student/								#
#	Contains a list of all students currently in the database	#
#	regardless of whether they are active or not.				#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['staff'])														# Restricted to users with 'staff' role.
@active_report()																			# Verifies active report, no effect for staff.
def teacher_student_list_view(request, *args, **kwargs):
	user_list = User.objects.filter(groups__name='student')
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
			profile_list.append(profile_dict)																		# Returns a list of all users in the database with the 
	content = {
		'profile_list': profile_list,														# with the group of student.
		'student_list': user_list
	}
	return render(request, 'teacher_student_list.html', content)


# ************************************************************* #
#																#
#  	URLpattern: teacher/student/<int:student_id>/				#
#	Views an individual student and details all information		#
#	including all entries, their reports and gives the teacher  #
#	the ability to allocate badges.								#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['staff'])														# Restricted to users with 'staff' role.
@active_report()																			# Verifies active report, no effect for staff.
def teacher_student_view(request, student_id, *args, **kwargs):
	try:
		student = User.objects.get(id=student_id)
	except:
		return HttpResponseRedirect("/teacher/student/")									# If user does not exist return user to list
	student_list = User.objects.filter(groups__name='student')
	if student not in student_list:															# Ensures that the when a teacher attempts to view
		return HttpResponseRedirect("/teacher/student/")

	student_details = {
		'student_details': student,
		'student_profile': None
	}
	try:	
		student_profile = Profile.objects.get(user=student)
		student_details['student_profile'] = student_profile
	except:
		pass																			# a student they can only access users from the 
	user_id = student_id  																	# student group.
	student_report = Report.objects.filter(student_id=student_id).annotate(num_entries=models.Count('entry'))
	student_badges = Allocation.objects.filter(student_id=student_id)
	student_entries = {}
	for report in student_report:															# Makes a single item dictionary with comment count added
		student_entries = Entry.objects.annotate(num_comments=models.Count('comment')).filter(report_id=report.report_id)
	content = {
		'student_details': student_details,
		'student': student,
		'student_reports': student_report,
		'student_entries': student_entries,
		'student_badges': student_badges,
		'student_id': user_id
	}
	return render(request, 'teacher_student.html', content)									# Renders view to teacher_student.html

