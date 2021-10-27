from django.shortcuts import render
# Create your views here.
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from views.views import student_dashboard_view, teacher_dashboard_view

#-------------------------------------------------------------------------------------------------------------------#
#                                              UNIVERSAL FUNCTIONS                                                  #
#-------------------------------------------------------------------------------------------------------------------#

# ************************************************************* #
#                                                               #
#   URLpattern: teacher/student/                                #
#   Contains a list of all students currently in the database   #
#   regardless of whether they are active or not.               #
#                                                               #
# ************************************************************* #

def page_login_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        uservalue=''
        passwordvalue=''
        form = LoginForm(request.POST or None)
        if form.is_valid():
            uservalue= form.cleaned_data.get("username")
            passwordvalue= form.cleaned_data.get("password")
            user = authenticate(username=uservalue, password=passwordvalue)
            if user is not None:
                login(request, user)
                context = {'form': form,
                          'error': 'The login has been successful'}
                if request.user.groups.all()[0].name == 'student':
                    return student_dashboard_view(request)
                elif request.user.groups.all()[0].name == 'staff':
                    return teacher_dashboard_view(request)
                else:
                    return HttpResponseRedirect("/")
            else:
                context = {'form': form,
                          'error': 'The username and password combination is incorrect'}
                return render(request, 'login.html', context )
        else:
            context= {'form': form,
                        'error': 'The form is not valid'
                        }
            return render(request, 'login.html', context)
    else:
        return render(request, 'logged_in.html', {} )

# ************************************************************* #
#                                                               #
#   URLpattern: teacher/student/                                #
#   Contains a list of all students currently in the database   #
#   regardless of whether they are active or not.               #
#                                                               #
# ************************************************************* #

def page_logout_view(request, *args, **kwargs):
    logout(request)
    return HttpResponseRedirect("/")

# ************************************************************* #
#                                                               #
#   URLpattern: teacher/student/                                #
#   Contains a list of all students currently in the database   #
#   regardless of whether they are active or not.               #
#                                                               #
# ************************************************************* #

def no_report_view(request, *args, **kwargs):
    return render(request, 'no_valid_report.html', {})