"""btswebdev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import contrib
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
#from btswebdev import bts_user
#from btswebdev.views.views import student_profile_view
from views import views 
from comment import views as comment_views
from entry import views as entry_views
from report import views as report_views
from badge import views as badge_views
from bts_user import views as bts_user_views
from login import views as login_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    #-------------------------------------------------------------------------------------------------------------------#
    #                                                      ADMIN                                                        #
    #-------------------------------------------------------------------------------------------------------------------#

    path('admin/', admin.site.urls),

    #-------------------------------------------------------------------------------------------------------------------#
    #                                                   LOGIN/LOGOUT                                                    #
    #-------------------------------------------------------------------------------------------------------------------#

    path('', login_views.page_login_view, name='login'),
    path('login',login_views.page_login_view, name='login'),
    path('logout/', login_views.page_logout_view, name='logout'),
    path('no_report/', login_views.no_report_view, name='no_report'),

    #-------------------------------------------------------------------------------------------------------------------#
    #                                                       TEACHER                                                     #
    #-------------------------------------------------------------------------------------------------------------------#
    # Below is a list of teacher or staff URLS that are formatted as such path(<'URL path'>, <desired function to call>,
    # <name parameter>) upon navigation to the inputted URL the function passed to the path will be called. See top of 
    # page for more detailed explaination of how to add additional urlpatterns.

    # ***************************************************************************************************************** #
    #                                       TEACHER DASHBOARD AND STUDENT LIST URLS                                     #  
    # ***************************************************************************************************************** #

    # View for the teacher dashboard
    path('teacher/', views.teacher_dashboard_view, name='teacher_dashboard'),
    # View showing the list of students and their details
    path('teacher/student/', bts_user_views.teacher_student_list_view, name='teacher_student_list'),
    # View for an individual student containing their recent entries and allocated badges.
    path('teacher/student/<int:student_id>/', bts_user_views.teacher_student_view, name='teacher_student'),

    # ***************************************************************************************************************** #
    #                                               TEACHER ENTRY URLS                                                  #  
    # ***************************************************************************************************************** #

    # View containing all of the most recent entries not sorted by any student.
    path('teacher/entry/', entry_views.teacher_entry_list_view, name='teacher_entry_list'),
    # View an individual students entry and add comment which is posted to the URL below this one
    path('teacher/entry/<int:entry_id>/', comment_views.teacher_comment_view, name='teacher_entry'),
    path('teacher/entry/<int:entry_id>/create/', comment_views.teacher_create_comment_view, name='teacher_entry'),
    # View for looking at a students list of entries
    path('teacher/student/<int:student_id>/entry/', entry_views.teacher_entry_single_list_view, name='teacher_entry'),
    

    # ***************************************************************************************************************** #
    #                                               TEACHER BADGE URLS                                                  #  
    # ***************************************************************************************************************** #

    # these paths are related to the badges
    path('teacher/badge/', badge_views.teacher_badge_view, name='teacher_badge_view'),
    path('teacher/badge/<int:badge_id>/', badge_views.teacher_single_badge_view, name='teacher_single_badge_view'),
    # View for looking at a students list of badges and allowing them to be allocated with the URL below
    path('teacher/student/<int:student_id>/badge/', badge_views.badge_teacher_allocation_list, name='teacher_allocate'),
    path('teacher/student/<int:student_id>/badge/<int:badge_id>/', badge_views.badge_create_allocation, name='teacher_allocate'),

    # ***************************************************************************************************************** #
    #                                               TEACHER REPORT URLS                                                 #  
    # ***************************************************************************************************************** #

    # View for the list of active student reports
    path('teacher/report/', report_views.report_view, name='report_view'),
    # View for looking at an individual student report the URL below views the report
    path('teacher/student/<int:student_id>/report/<int:report_id>/', report_views.single_report_view, name='report_view'),
    path('teacher/student/<int:student_id>/report/<int:report_id>/view', report_views.render_pdf_view, name='pdf_view'),
    # path('teacher/reports/<username>', report_views.teacher_single_student_view, name='single_student_view'),
   
    
    #---------------------------------------------------------------------------------------------------------------------#
    #                                                    STUDENTS                                                         #
    #---------------------------------------------------------------------------------------------------------------------#
    # Below is the collection of URLs used by students in the same format as above. If additions or changes need to be made
    # please refer to the instructions at the top of the page.

    # ***************************************************************************************************************** #
    #                                               STUDENT DASHBOARD URL                                               #  
    # ***************************************************************************************************************** #

    path('student/', views.student_dashboard_view, name='student_dashboard'),

    # ***************************************************************************************************************** #
    #                                               STUDENT ENTRY URLS                                                  #  
    # ***************************************************************************************************************** #

    path('student/entry/', entry_views.student_entry_list_view, name='student_entry'),
    path('student/entry/<int:entry_id>/', entry_views.student_entry_view, name='student_entry'),
    path('student/entry/<int:entry_id>/edit', entry_views.student_edit_entry_view, name='student_entry_edit'),
    path('student/entry/create', entry_views.student_create_entry_view, name='student_create_entry' ),
    path('student/entry/<int:entry_id>/edit/delete', entry_views.student_entry_delete, name='student_entry_delete'),
    path('student/entry/<int:entry_id>/edit/image/<int:image_id>/delete', entry_views.delete_entry_image_view, name='student_delete_image'),

    # ***************************************************************************************************************** #
    #                                               STUDENT BADGE URLS                                                  #  
    # ***************************************************************************************************************** #

    path('student/badge/', badge_views.badge_list_view, name='badge_list'),
    path('student/badge/<int:badge_id>/', badge_views.badge_view, name='badge_view'),

    # ************************************************************************************************************** #
    #                                               STUDENT PROFILE URLS                                             #  
    # ************************************************************************************************************** #

    path('student/profile/', views.student_profile_view, name='student_profile_view'),




    # ***************************************************************************************************************** #
    #                                               TEACHER REPORT URLS                                                 #  
    # ***************************************************************************************************************** #

    path('student/reports/<filename>', report_views.student_report_view, name='view_files'),
    path('student/reports/', report_views.student_report_list_view, name='report_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



