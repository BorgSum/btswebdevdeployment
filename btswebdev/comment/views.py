from django.shortcuts import render
from entry.models import Entry, EntryImage
from comment.models import Comment, CommentImage
from django.contrib.auth.models import User
from django.db import models
from .forms import RawCommentForm
from django.contrib.auth.decorators import login_required
from login.decorators import allowed_users, active_report
from django.http import HttpResponseRedirect


#-------------------------------------------------------------------------------------------------------------------#
#                                              TEACHER FUNCTIONS                                                    #
#-------------------------------------------------------------------------------------------------------------------#


# ************************************************************* #
#																#
#  	URLpattern: teacher/entry/<int:entry_id>/					#
#	Displays a single student entry and presents the user 		#
# 	with the comment form to add comments to an entry_id.		#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['staff'])														# Restricted to users with 'staff' role.
@active_report()																			# Verifies active report, no effect for staff.
def teacher_comment_view(request, entry_id, *args, **kwargs):
	user = request.user.id 																	# Sets user to be the currently logged in user.
	comment_form = RawCommentForm()															
	student_entries = Entry.objects.get(entry_id=entry_id)									# Gets the entry specified in the <int:entry_id>.
	entry_comment = Comment.objects.select_related('staff_id').filter(entry_id=entry_id) 	# Gets comments associated with the specified entry.
	image_list =  EntryImage.objects.select_related('entry_id').filter(entry_id=entry_id) 	# Gets the list of images associated with the entry.
	comment_list = []
	for comment in entry_comment:															# Iterates through the all the comments and adds
		comment_images = CommentImage.objects.filter(comment_id=comment)					# and found images to a list of dictionaries with 
		comment_dict = {																	# the comment query set object under the key 'comment'	
			'comment': comment,																# and the query set of comment images under the key				
			'comment_image': comment_images													# 'comment_images' this is so that the images are 
		}																					# are paired with the right comment.		
		comment_list.append(comment_dict)
	if not entry_comment:																	# Sets the entry comment to "" if no comments are found   
		entry_comment = ""																	# for the selected entry.
	content = {																				
		'query_set': student_entries,														# Defines the content in a dictionary to pass to the HTML
		'comment_set': comment_list,														# page to render.
		'form': comment_form,
		'image_set': image_list
	}
	return render(request, 'teacher_entry.html', content)									# Passes the content dictionary to 'teacher_entry.html'


# ************************************************************* #
#																#
#  	URLpattern: teacher/entry/<int:entry_id>/create/			#
#	Is called when the teacher creates a new comment 			#
# 	creates a new comment in the database as well as new		#
#   comment images as well										#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['staff'])														# Restricted to users with 'staff' role.
@active_report()																			# Verifies active report, no effect for staff.
def teacher_create_comment_view(request, entry_id, *args, **kwargs):
	valid_file_formats = ('.jpg','.jpeg','.png')											# Defines the valid image formats for uploaded files
	user = request.user.id																	# Sets user to be the currently logged in user.
	comment_form = RawCommentForm()
	if request.method == "POST":															# Only runs if the request method is POST.
		comment_form = RawCommentForm(request.POST)											# Passes the comment form the values contained in the POST request.
		if comment_form.is_valid():															# Only runs if the form is valid otherwise returns to teacher dashboard.
			# Creates a new comment with the cleaned form data and giving it the entry object for the current entry and the currently logged in user.
			comment = Comment.objects.create(**comment_form.cleaned_data, entry_id=Entry.objects.get(entry_id=entry_id), staff_id=User.objects.get(id=user))
			images = request.FILES.getlist('images')										
			for image in images:															# Goes through each image and checks the uploaded
				if str(image).endswith(valid_file_formats):									# file extensions. If valid creates a new comment 
					photo = CommentImage.objects.create(									# image associated with the newly created comment.
						comment_id=comment,
						comment_image_file=image
					)						
				else:
					return HttpResponseRedirect(f"/teacher/entry/{ entry_id }/")			# If image format is incorrect the images will not upload
			return HttpResponseRedirect(f"/teacher/entry/{ entry_id }/")					# Once created the user will be redirected to the entry.
	return HttpResponseRedirect("/teacher/")