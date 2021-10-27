from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from login.decorators import allowed_users, active_report
from .forms import ReportForm
from django.contrib.auth.models import User
from comment.models import Comment, CommentImage
from .models import Report, GeneratedReport
from badge.models import Badge, Allocation
from django.http import HttpResponseRedirect
from entry.models import Entry, EntryImage
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
import datetime

# imports required for the pdf generation
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# imports for saving the generated pdf
from django.core.files import File
from io import BytesIO
from io import StringIO

#-------------------------------------------------------------------------------------------------------------------#
#                                              TEACHER FUNCTIONS                                                    #
#-------------------------------------------------------------------------------------------------------------------#

# ************************************************************* #
#																#
#  	URLpattern: teacher/report									#
#	Displays a list of all of the reports for all students 		#
#	as long as the report is active. 							#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['staff'])														# Restricted to users with 'staff' role.
@active_report()																			# Verifies active report, no effect for staff.
def report_view(request, *args, **kwargs):
	student_list = User.objects.filter(groups__name='student') 								# Filters the students by the django group they are apart of
	student_report = Report.objects.filter(report_active=True)								# Only obtains student reports that are active
	content = {
		'student_list': student_list,
		'student_reports': student_report
	}
	return render(request, 'report.html', content)											# Renders the content to report.html


# *************************************************************************	#
#																			#
#  	URLpattern: teacher/student/<int:student_id>/report/<int:report_id>/	#
#	Displays a single selected report from a given student and				#
#	contains the textarea to add additional comments.						#
#																			#
# *************************************************************************	#

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['staff'])														# Restricted to users with 'staff' role.
@active_report()																			# Verifies active report, no effect for staff.
def single_report_view(request, student_id, report_id, *args, **kwargs):
	selected_student = User.objects.get(id=student_id)										# Gets selected student
	selected_report = Report.objects.get(report_id=report_id)								# Gets selected report
	content = {
		'student': selected_student,
		'report': selected_report
	}
	return render(request, 'single_report.html', content)									# Renders the content to single_report.html

	
# *************************************************************************	#
#																			#
#  URLpattern: teacher/student/<int:student_id>/report/<int:report_id>/view #
#  Gets all of the student entries and associated comments and badges 		#
#  and uses xhtml2pdf to change it into a pdf file and saves it as 			#
#  generated pdf so the student can access them. The function also takes	#
#  the additional comments that the staff member posted.					#
#																			#
# *************************************************************************	#

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['staff'])														# Restricted to users with 'staff' role.
@active_report()																			# Verifies active report, no effect for staff.
def render_pdf_view(request, student_id, report_id, *args, **kwargs):
	if request.method == "POST":
		additional_comments = request.POST['addComment']									# Gets the additional comments field
		teacher = User.objects.get(id=request.user.id)
		template_path = 'pdf1.html'															# Defines the html file that will act as the template for the pdf
		selected_student = User.objects.get(id=student_id)
		selected_report = Report.objects.get(student_id=selected_student, report_id=report_id)
		selected_report.report_additional_comment = additional_comments
		selected_report.save()																# Once updates to the reports additional comments field
		selected_entries = Entry.objects.filter(report_id=selected_report)					# have been made it is saved.
		image_list = []
		comment_list = []
		teacher_images = []
		obtained_badges = Allocation.objects.filter(student_id=selected_student, alloc_date__range=[selected_report.report_start_date, selected_report.report_end_date])
		for entry in selected_entries:														# For every entry gets all associated images and comments
			current_image = EntryImage.objects.filter(entry_id=entry)						# and places them in an array associated with each entry.
			current_comment = Comment.objects.filter(entry_id=entry)
			image_list.append(current_image)
			comment_list.append(current_comment)
			for comment in current_comment:
				current_teacher_image = CommentImage.objects.filter(comment_id=comment)
				teacher_images.append(current_teacher_image)
		context = {
			'additional_comments': additional_comments,
			'teacher_images': teacher_images,
			'student_details': selected_student,
			'teacher_details': teacher,
			'report_entries': selected_entries,
			'report_details': selected_report,
			'comment_list': comment_list,
			'image_list': image_list,
			'badge_list': obtained_badges 
		}

		response = HttpResponse(content_type='application/pdf')								# Sets the response to be a pdf

		#if you need to download the pdf:
		# repsonse['Content-Disposition'] = f'attachment; filename="{user_name}.pdf"'
		# if you need to just view the pdf:
		response['Content-Disposition'] = f'filename="{selected_student.first_name}_report.pdf"'
		template = get_template(template_path)
		html = template.render(context)
		file_path = f'{selected_student.first_name}_{selected_student.last_name}_{selected_report.report_start_date}-{selected_report.report_end_date}_report.pdf'
		result = open(f'media\\reports\\{file_path}', 'wb')
		pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
		
		# creates the pdf
		pisa_status = pisa.CreatePDF(html, dest=response)
		if pisa_status.err:
			return HttpResponse("We had some errors <pre>" + html + "</pre>")
		try:
			existing_student_report = GeneratedReport.objects.get(gen_student_id=selected_student, gen_report_start_date=selected_report.report_start_date,gen_report_end_date=selected_report.report_end_date)
			existing_student_report.gen_report_file = file_path
			existing_student_report.save()											# Tries to select a generated report if it already exists it updates the file
		except ObjectDoesNotExist:													# if the generated report is not found the exception is caught and it creates
			created_report = GeneratedReport(										# a new generated report and saves it to the database 
				 gen_report_start_date=selected_report.report_start_date,
				 gen_report_end_date=selected_report.report_end_date,
				 gen_student_id=selected_student,
				 gen_report_file=file_path)
			result.close()
			created_report.save()
		return response  															# Returns the pdf repsonse 


#-------------------------------------------------------------------------------------------------------------------#
#                                              STUDENT FUNCTIONS                                                    #
#-------------------------------------------------------------------------------------------------------------------#


# ************************************************************* #
#																#
#  	URLpattern: student/reports/								#
#	Displays a list of reports that are generated for the 		#
#	logged in student. And the date to organise the current 	#
#	report.  													#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['student'])													# Restricted to users with 'student' role.
@active_report()																			# Verifies active report, redirects user if report is false.
def student_report_list_view(request, *args, **kwargs):
	user = request.user.id
	report_list = GeneratedReport.objects.filter(gen_student_id=user)						# Gets list of reports associated with logged in user
	current_date = datetime.date.today()													# gets the current date
	content = {
		'report_list': report_list,
		'current_date': current_date
	}
	return render(request, 'student_report_list.html', content)								# Renders the content to student_report_list.html


# ************************************************************* #
#																#
#  	URLpattern: student/reports/<filename>						#
#	Gets the PDF stored under the desired name and returns		#
#	the pdf response.											#
#																#
# ************************************************************* #

@login_required(login_url='/')																# Redirects if not logged in.
@allowed_users(allowed_roles=['student'])													# Restricted to users with 'student' role.
@active_report()																			# Verifies active report, redirects user if report is false.
def student_report_view(request, filename, *args, **kwargs):
	return FileResponse(open(f'media\\reports\\{filename}', 'rb'), content_type='application/pdf')	# Opens the file stored at that location
