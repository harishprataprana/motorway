"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views, Hod_Views, Staff_Views, Student_Views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('base/', views.BASE, name='base'),
                  path('get_current_time/', views.GET_CURRENT_TIME, name='get_current_time'),
                  path('convert_timezones/', views.convert_timezones, name='convert_timezones'),

                  # Login Path
                  path('', views.LOGIN, name='login'),
                  path('doLogin', views.doLogin, name='doLogin'),
                  path('doLogout', views.doLogout, name='logout'),

                  # Profile Section
                  path('profile', views.PROFILE, name='profile'),
                  path('profile/update', views.PROFILE_UPDATE, name='profile_update'),

                  # HOD Panel Paths
                  path('HOD/home', Hod_Views.HOME, name='hod_home'),
                  path('HOD/student/add', Hod_Views.ADD_STUDENT, name='add_student'),
                  path('HOD/student/view', Hod_Views.VIEW_STUDENT, name='view_student'),
                  path('HOD/student/edit/<str:id>', Hod_Views.EDIT_STUDENT, name='edit_student'),
                  path('HOD/student/update', Hod_Views.UPDATE_STUDENT, name='update_student'),
                  path('HOD/student/delete/<str:admin>', Hod_Views.DELETE_STUDENT, name='delete_student'),

                  path('HOD/staff/add', Hod_Views.ADD_STAFF, name='add_staff'),
                  path('HOD/staff/view', Hod_Views.VIEW_STAFF, name='view_staff'),
                  path('HOD/staff/edit/<str:id>', Hod_Views.EDIT_STAFF, name='edit_staff'),
                  path('HOD/staff/update', Hod_Views.UPDATE_STAFF, name='update_staff'),
                  path('HOD/staff/delete/<str:admin>', Hod_Views.DELETE_STAFF, name='delete_staff'),

                  path('HOD/course/add', Hod_Views.ADD_COURSE, name='add_course'),
                  path('HOD/course/view', Hod_Views.VIEW_COURSE, name='view_course'),
                  path('HOD/course/edit/<str:id>', Hod_Views.EDIT_COURSE, name='edit_course'),
                  path('HOD/course/update', Hod_Views.UPDATE_COURSE, name='update_course'),
                  path('HOD/course/delete/<str:id>', Hod_Views.DELETE_COURSE, name='delete_course'),

                  path('HOD/Staff/SendNotification', Hod_Views.STAFF_SEND_NOTIFICATION, name='staff_send_notification'),
                  path('HOD/Staff/SaveNotification', Hod_Views.SAVE_STAFF_NOTIFICATION, name='save_staff_notification'),

                  # Staff Panel Paths
                  path('Staff/home', Staff_Views.HOME, name='staff_home'),
                  path('Staff/Notifications', Staff_Views.NOTIFICATIONS, name='notifications'),
                  path('Staff/Notifications/Mark_read/<str:status>', Staff_Views.NOTIFICATIONS_MARK_READ, name='notifications_mark_read')




              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
