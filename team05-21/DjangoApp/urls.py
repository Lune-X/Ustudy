"""DjangoApp URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from Accounts.views import login_page, logout_page, login_form, gdpr_page, register
from Profile.views import module_dashboard_page, choose_school_page, choose_course_page, user_profile_page, edit_profile_page
from Videos.views import list_videos_page, post_video_page, one_video_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', login_page),
    path('login/', login_page),
    path('logout/', logout_page),
    path('login/submit-form/', login_form),
    path('gdpr/', gdpr_page),
    path('module-dashboard/', module_dashboard_page),
    path('list-videos/', list_videos_page),
    path('post-video/', post_video_page),
    path('one-video/', one_video_page),
    path('register/', register),
    path('choose-school/', choose_school_page),
    path('choose-course/', choose_course_page),
    path('user-profile/', user_profile_page),
    path('edit-profile/', edit_profile_page)
]
