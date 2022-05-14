import logging

from django.shortcuts import render
from django.shortcuts import redirect


# Create your views here.
def module_dashboard_page(request):
    return render(request, 'Profile/module-dashboard.html')

def choose_school_page(request):
    return render(request, 'Profile/choose-school.html')

def choose_course_page(request):
    return render(request, 'Profile/choose-course.html')

def user_profile_page(request):
    return render(request, 'Profile/user-profile.html')

def edit_profile_page(request):
    return render(request, 'Profile/edit-profile.html')