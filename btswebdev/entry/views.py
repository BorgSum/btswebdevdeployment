from django.shortcuts import render
from entry.models import Entry, EntryImage
from comment.models import Comment
from django.contrib.auth.models import User
from django.db import models
from report.models import Report
from .forms import EntryForm, EntryImageForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from login.decorators import allowed_users, active_report
from badge.models import Allocation, Badge
from bts_user.models import Profile


#-------------------------------------------------------------------------------------------------------------------#
#                                              STUDENT FUNCTIONS                                                    #
#-------------------------------------------------------------------------------------------------------------------#

# ************************************************************* #
#																#
#  	URLpattern: student/entry/create							#
#	When directed to the above URL an entry is created for 		#
#	the currently logged on student as well as any entry image 	#
#	objects as well.											#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['student'])													# Restricted to users with 'student' role.
@active_report()																			# Verifies active report, redirects user if report is false.
def student_create_entry_view(request, *args, **kwargs):
	valid_file_formats = ('.jpg','.jpeg','.png')											# Sets the valid formats for the images to be the strings listed
	entry_form = EntryForm() 
	user = User.objects.get(id=request.user.id)
	active_report = Report.objects.get(student_id=user, report_active=True)								
	if request.method == "POST":							
		entry_form = EntryForm(request.POST)												# If the request method is POST then the entry will be created				
		if entry_form.is_valid():															# as well as any images, however if the images are not of the
			entry = entry_form.save(commit=False)											# correct format they are not created.
			entry.report_id = active_report
			entry.save()						
			images = request.FILES.getlist('images')	
			for image in images:	
				print(image)
				if str(image).endswith(valid_file_formats):
					photo = EntryImage.objects.create(		
							entry_id=entry,
							entry_image_file=image
							)						
			return HttpResponseRedirect('/student/entry/')										# Returns the user home once they create an entry
	content = {'entry_form': entry_form}
	return render(request, 'student_create_entry.html', content)


# ************************************************************* #
#																#
#  	URLpattern: student/entry/<int:entry_id>/edit				#
#	When directed to that URL the user will be able to edit   	#
#  	the entry id that is given to the URL granted that entry 	#
#	is in the same report as the currently logged in user.		#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['student'])													# Restricted to users with 'student' role.
@active_report()																			# Verifies active report, redirects user if report is false.
def student_edit_entry_view(request, entry_id, *args, **kwargs):
	valid_file_formats = ('.jpg','.jpeg','.png')
	user = request.user.id
	edit_entry = Entry.objects.get(entry_id=entry_id)			
	report = Report.objects.get(student_id=user, report_active=True)
	if edit_entry.report_id.report_id == report.report_id:
		entry_form = EntryForm(instance=edit_entry)					
		if request.method == "POST":								
			entry_form = EntryForm(request.POST, instance=edit_entry)
			if entry_form.is_valid():
				entry = entry_form.save()
				images = request.FILES.getlist('images')		
				desc = request.POST.get('desc')
				for image in images:	
					if str(image).endswith(valid_file_formats):						
						photo = EntryImage.objects.create(			
								entry_id=entry,
								entry_image_file=image
								)
				return HttpResponseRedirect(reverse('student_entry', args=[entry_id]) )
		else:
			image_list =  EntryImage.objects.select_related('entry_id').filter(entry_id=entry_id)
			content = {													
				'entry_form': entry_form,
				'entry_id': edit_entry.entry_id,					
				'query_set': edit_entry,
				'image_list': image_list
				}
			return render(request, 'student_edit_entry.html', content)
	else:
		return HttpResponseRedirect("/home/")


# ************************************************************* #
#																#
#  	URLpattern: student/entry/<int:entry_id>/ 					#
#	When the user is directed to this URL they are able to view #
#	the entry that is passed in as an entry id. 				#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['student'])													# Restricted to users with 'student' role.
@active_report()																			# Verifies active report, redirects user if report is false.
def student_entry_view(request, entry_id, *args, **kwargs):
	user = request.user.id
	report = Report.objects.get(student_id=user, report_active=True)
	student_entries = Entry.objects.get(entry_id=entry_id)
	entry_images = EntryImage.objects.select_related('entry_id').filter(entry_id=entry_id)
	entry_comment = Comment.objects.select_related('staff_id').filter(entry_id=entry_id)
	if student_entries.report_id.report_id == report.report_id:
		if not entry_comment:
			entry_comment = ""
		content = {
				'query_set': student_entries,
				'comment_set': entry_comment,
				'image_set': entry_images
		}
		return render(request, 'student_entry.html', content)
	else:
		return HttpResponseRedirect("/home/")


# ************************************************************* #
#																#
#  	URLpattern: student/entry/<int:entry_id>/edit/delete		#
#	When directed to this URL it will delete the entry that		#
# 	that is passed in as the entry id. 							#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['student'])													# Restricted to users with 'student' role.
@active_report()																			# Verifies active report, redirects user if report is false.
def student_entry_delete(request, entry_id, *args, **kwargs):
	if request.method == "POST":
		user = User.objects.get(id=request.user.id) 
		user_report = Report.objects.get(report_active=True, student_id=user.id)
		user_entries = Entry.objects.filter(report_id=user_report.report_id)
		deleted_entry = Entry.objects.get(entry_id=entry_id)
		if deleted_entry in user_entries:
			student_entry = Entry.objects.get(entry_id=entry_id)		
			student_entry.delete()										
			return HttpResponseRedirect("/student/entry/") 
		return HttpResponseRedirect("/student/entry/") 							
	return HttpResponseRedirect("/") 



# ***************************************************************************************** #
#																							#
#  	URLpattern: student/entry/<int:entry_id>/edit/image/<int:image_id>/delete				#
#	When directed to that URL the user will be able to delete the image that 				#
#	will be deleted will be the one passed in as the image. The entry id has no effect		#
# 	this.																					#
#																							#
# ***************************************************************************************** #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['student'])													# Restricted to users with 'student' role.
@active_report()																			# Verifies active report, redirects user if report is false.
def delete_entry_image_view(request, image_id, *args, **kwargs):
	if request.method == "POST":
		entry_image = EntryImage.objects.get(entry_image_id=image_id)
		assocaited_entry= Entry.objects.get(entry_id=entry_image.entry_id.entry_id)
		entry_image.delete()
		return HttpResponseRedirect(f"/student/{assocaited_entry.get_absolute_url()}/edit")
	return HttpResponseRedirect("/")



# ************************************************************* #
#																#
#  	URLpattern: student/entry/									#
#	When directed to that URL the user will be displayed all 	#
# 	entries that are in the currently active report for the 	#
#	the currently logged in user.								#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['student'])													# Restricted to users with 'student' role.
@active_report()																			# Verifies active report, redirects user if report is false.
def student_entry_list_view(request, *args, **kwargs):
	user = request.user.id
	report = Report.objects.get(student_id=user, report_active=True)
	student_entries = Entry.objects.annotate(num_comments=models.Count('comment')).filter(report_id=report).order_by('-entry_date')
	content = {
			'query_set': student_entries		
	}
	return render(request, 'student_entry_list.html', content)


#-------------------------------------------------------------------------------------------------------------------#
#                                              TEACHER FUNCTIONS                                                    #
#-------------------------------------------------------------------------------------------------------------------#

@login_required(login_url='/')
@allowed_users(allowed_roles=['staff'])
@active_report()
def teacher_entry_list_view(request, *args, **kwargs):
	student_entries = Entry.objects.annotate(num_comments=models.Count('comment')).order_by('-entry_date')
	content = {
			'entry_list': student_entries		
	}
	return render(request, 'teacher_entry_list.html', content)


@login_required(login_url='/')
@allowed_users(allowed_roles=['staff'])
@active_report()
def teacher_entry_single_list_view(request, student_id, *args, **kwargs):
	user = User.objects.get(id=student_id)
	report = Report.objects.get(student_id=user, report_active=True)
	student_entries = Entry.objects.filter(report_id=report).annotate(num_comments=models.Count('comment')).order_by('-entry_date')
	content = {
			'entry_list': student_entries		
	}
	return render(request, 'teacher_entry_list.html', content)
			