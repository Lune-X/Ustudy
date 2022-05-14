import logging

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm


# Create your views here.

# REGISTER PAGE RELATED
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        else:
            return redirect('/register/')
    else:
        form = RegisterForm()

    return render(response, 'Accounts/register.html', {'form':form})
    
# LOGIN / LOGOUT PAGE RELATED
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/module-dashboard/') 
    return render(request, 'Accounts/login.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')


def login_form(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

       
        if user is not None:
            login(request, user)
            return redirect('/module-dashboard/')
        else:
            return redirect('/login/')

    return redirect('/login/')


def gdpr_page(request):
    return render(request, 'Accounts/gdpr.html')

def choose_school(request):
    return render(request, 'Accounts/choose-school.html')
