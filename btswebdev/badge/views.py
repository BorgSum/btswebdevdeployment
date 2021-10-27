from django.shortcuts import render
from .models import Badge, Allocation
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from login.decorators import allowed_users, active_report
from django.contrib.auth.models import User

#-------------------------------------------------------------------------------------------------------------------#
#                                              TEACHER FUNCTIONS                                                    #
#-------------------------------------------------------------------------------------------------------------------#



# ************************************************************* #
#																#
#  	URLpattern: teacher/student/<int:student_id>/badge/			#
#	Directs teacher to a page that list all badges and allows  	#
#	for the allocation of badges to the student they			#
# 	are viewing.												#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['staff'])														# Restricted to users with 'staff' role.
@active_report()																			# Verifies active report, no effect for staff.
def badge_teacher_allocation_list(request, student_id, *args, **kwargs):
	alloc_list = Allocation.objects.filter(student_id=student_id)
	url_id = student_id
	badge_list = Badge.objects.all()
	item_list = []
	student = User.objects.get(id=student_id)
	for badge in badge_list:
		item_list.append({"obtained": False, "badge": badge, "alloc": None})
	for alloc in alloc_list:
		for item in item_list:
			if item['badge'].badge_id == alloc.badge_id.badge_id:
				item['obtained'] = True
				item['alloc'] = alloc
	content = {
		'student_details': student,
		'item_list': item_list,
		'student_id': url_id
	}
	return render(request, 'teacher_student_badge_list.html', content)


# *********************************************************************	#
#																		#
#  	URLpattern: teacher/student/<int:student_id>/badge/<int:badge_id>/	#
#	The URL that creates the allocation object upon being pointed to	#
#																		#
# *********************************************************************	#

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['staff'])														# Restricted to users with 'staff' role.
@active_report()																			# Verifies active report, no effect for staff.
def badge_create_allocation(request, student_id, badge_id, *args, **kwargs):
	if request.method == "POST":															# If the request method is POST						
		user = request.user.id
		student = User.objects.get(id=student_id)
		badge = Badge.objects.get(badge_id=badge_id)
		staff = User.objects.get(id=user)
		Allocation.objects.create(student_id=student, badge_id=badge, staff_id=staff)		# Creates an allocation object
		return HttpResponseRedirect("/teacher/student/" + str(student_id) +"/badge")		# redirects the staff member to the student page

	return HttpResponseRedirect("/teacher/student/" + str(student_id) +"/badge")


# *********************************************************************	#
#																		#
#  	URLpattern: teacher/badge/											#
#	Gets a list of all badges that are in the database with the ability	#
#	to view details on them.											#
#																		#
# *********************************************************************	#

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['staff'])														# Restricted to users with 'staff' role.
@active_report()																			# Verifies active report, no effect for staff.
def teacher_badge_view(request, *args, **kwargs):
	badge_list = Badge.objects.all()														
	content = {
		'badge_list': badge_list
	}
	return render(request, 'teacher_badge_view.html', content)								# Renders content at teacher_badge_view.html


# *********************************************************************	#
#																		#
#  	URLpattern: teacher/badge/<int:badge_id>/							#
#	Gets a single badge and provides details on which students have		#
# 	the badge allocated and which do not allows for another way of mass	#
#	allocating badges to student. 										#
#																		#
# *********************************************************************	#

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['staff'])														# Restricted to users with 'staff' role.
@active_report()																			# Verifies active report, no effect for staff.
def teacher_single_badge_view(request, badge_id, *args, **kwargs):
	badge_info = Badge.objects.get(badge_id=badge_id)										# Gets badge as defined in URL.
	student_list = User.objects.filter(groups__name='student')								# Gets all student Users.
	badge_list = Badge.objects.all()
	unalloc_list = []
	for student in student_list:
		unalloc_list.append(student)														# Adds all students to a array called unalloc_list

	for student in student_list:
		try:																				# Tries to find an allocation for the badge for the 
			alloc = Allocation.objects.get(badge_id=badge_info, student_id=student)			# current student, if it does it removes them from 
			print(f"student {student.first_name} to be removed")							# the list. Otherwise the student remains on the 
			unalloc_list.remove(student)													# list as there is no allocation for them.
		except:
			print(f"Except for {student.first_name} ")
		
	content = {
		'badge_info': badge_info,
		'unalloc_list': unalloc_list
	}
	return render(request, 'teacher_single_badge_view.html', content)						# Renders content to teacher_single_badge_view.html


#-------------------------------------------------------------------------------------------------------------------#
#                                              STUDENT FUNCTIONS                                                    #
#-------------------------------------------------------------------------------------------------------------------#

# ************************************************************* #
#																#
#  	URLpattern: student/reports/								#
#	N/A Not sure												#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['student'])													# Restricted to users with 'student' role.
@active_report()																			# Verifies active report, redirects user if report is false.
def badge_view(request, badge_id, *args, **kwargs):
	user = request.user
	alloc_list = Allocation.objects.filter(student_id=user)
	badge = Badge.objects.get(badge_id=badge_id)
	badge_list = Badge.objects.all()
	badge_info = {
		'obtained': False,
		'badge': badge,
		'alloc': None 
	}
	for alloc in alloc_list:
		if badge.badge_id == alloc.badge_id.badge_id:
			badge_info['obtained'] = True
			badge_info['alloc'] = alloc
			break

	content = {
		'item': badge_info
	}
	return render(request, 'student_badge_view.html', content)


# ************************************************************* #
#																#
#  	URLpattern: student/reports/								#
#	N/A Not sure												#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['student'])													# Restricted to users with 'student' role.
@active_report()																			# Verifies active report, redirects user if report is false.
def badge_list_view(request, *args, **kwargs):
	user = request.user
	alloc_list = Allocation.objects.filter(student_id=user)
	#print(alloc_list)
	badge_list = Badge.objects.all()
	item_list = []
	for badge in badge_list:
		item_list.append({"obtained": False, "badge": badge, "alloc": None})
	for alloc in alloc_list:
		for item in item_list:
			if item['badge'].badge_id == alloc.badge_id.badge_id:
				item['obtained'] = True
				item['alloc'] = alloc
	content = {
		'item_list': item_list
	}
	return render(request, 'student_badge_list.html', content)





