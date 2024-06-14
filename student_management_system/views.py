from datetime import timedelta

from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CustomUser
from django.http import JsonResponse
from django.utils import timezone
import pytz


def BASE(request):
    return render(request, 'base.html')


def GET_CURRENT_TIME(request):
    current_time = timezone.now()
    new_time = current_time + timedelta(hours=5, minutes=30)
    formatted_time = new_time.strftime('%A, %B %d, %Y %H:%M:%S %p')
    return JsonResponse({'current_time': formatted_time})


def convert_timezones(request):
    # Get the current time in UTC
    utc_time = timezone.now()

    # Convert to IST (Indian Standard Time)
    ist = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))

    # Convert to EST (Eastern Standard Time)
    est = utc_time.astimezone(pytz.timezone('US/Eastern'))

    # Convert to CST (Central Standard Time)
    cst = utc_time.astimezone(pytz.timezone('US/Central'))

    # Convert to PST (Pacific Standard Time)
    pst = utc_time.astimezone(pytz.timezone('US/Pacific'))

    # Convert to MST (Mountain Standard Time)
    mst = utc_time.astimezone(pytz.timezone('US/Mountain'))

    # Convert to GMT (Greenwich Mean Time)
    gmt = utc_time.astimezone(pytz.timezone('GMT'))

    response_data = {
        'utc_time': utc_time.strftime('%A, %B %d, %Y %H:%M:%S %Z'),
        'ist_time': ist.strftime('%A, %B %d, %Y %H:%M %Z'),
        'est_time': est.strftime('%A, %B %d, %Y %H:%M %Z'),
        'cst_time': cst.strftime('%A, %B %d, %Y %H:%M %Z'),
        'pst_time': pst.strftime('%A, %B %d, %Y %H:%M %Z'),
        'mst_time': mst.strftime('%A, %B %d, %Y %H:%M %Z'),
        'gmt_time': gmt.strftime('%A, %B %d, %Y %H:%M %Z'),
    }

    return JsonResponse(response_data)


def LOGIN(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password'), )

        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('hod_home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return HttpResponse('This is Student Panel')
            else:
                messages.error(request, 'Email or Password Is Invalid !')
                return redirect('login')
        else:
            messages.error(request, 'Email or Password Is Invalid !')
            return redirect('login')


def doLogout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user,
    }
    # file_path = user.profile_pic.path
    # print(file_path)
    return render(request, 'profile.html', context)


@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        # username = request.POST.get('username')
        password = request.POST.get('password')
        profile_pic = request.FILES.get('profile_pic')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password is not None and password != "":
                customuser.set_password(password)
            if profile_pic is not None:
                customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, 'Profile Updated Successfully !')
            return redirect('profile')

        except:
            messages.error(request, 'Something Went Wrong, Please try again !')

    return render(request, 'profile.html')






