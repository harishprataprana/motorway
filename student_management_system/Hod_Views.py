import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from app.models import Course, Session, Student, CustomUser, Staff, Staff_Notification
from django.contrib import messages
from app.decorators import admin_required
from django.utils import timezone


# def check_admin(user):
#     return user.is_superuser


# @user_passes_test(check_admin)
@admin_required
@login_required(login_url='/')
def HOME(request):
    current_time = timezone.now()

    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()

    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()



    context = {
        "current_time": current_time,
        "student_count": student_count,
        "staff_count": staff_count,
        "course_count": course_count,
        "student_gender_male": student_gender_male,
        "student_gender_female": student_gender_female,
    }
    return render(request, 'Hod/home.html', context)


@admin_required
@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()
    session_year = Session.objects.all()
    # print(course)
    # print(session_year)

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'This Email is already registered !')
            return redirect('add_student')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'This Username is already registered !')
            return redirect('add_student')

        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                profile_pic=profile_pic,
                user_type=3,
            )
            user.set_password(password)
            user.save()

            course = Course.objects.get(id=course_id)
            session_year = Session.objects.get(id=session_year_id)

            student = Student(
                admin=user,
                address=address,
                session_year_id=session_year,
                course_id=course,
                gender=gender,
            )
            student.save()
            messages.success(request, user.first_name + " " + user.last_name + ' Successfully added !')
            return redirect('add_student')

    #     grade = request.POST.get('grade')
    #     country = request.POST.get('country')
    #     phone = request.POST.get('phone')
    #     email = request.POST.get('email')
    #
    #     registered_on = request.POST.get('registered_on')
    #     registered_upto = request.POST.get('registered_upto')

    #     selected_courses_ids = request.POST.getlist('courses')
    #     selected_courses_ids = [int(course_id) for course_id in selected_courses_ids]
    #     selected_courses = Course.objects.filter(id__in=selected_courses_ids)
    #     selected_courses_names = [course.name for course in selected_courses]
    #
    #     if CustomUser.objects.filter(email=email).exists():
    #         messages.warning(request, 'This Email is already registered !')
    #         return redirect('add_student')
    #     else:
    #         user = CustomUser(
    #             first_name=student_name,
    #             last_name=parent_name,
    #             username=username,
    #             email=email,
    #             profile_pic=profile_pic,
    #             user_type=3,
    #         )
    #         user.set_password = password
    #         user.save()
    #
    #         student = Student(
    #             admin=user,
    #             name=student_name,
    #             parent_name=parent_name,
    #             gender=gender,
    #             grade=grade,
    #             country=country,
    #             mobile=phone,
    #             registered_on=registered_on,
    #             registered_upto=registered_upto,
    #         )
    #         student.save()
    #         courses=Course.objects.filter(name__in=selected_courses_names),
    #         student.courses.set(courses)
    #         return redirect('add_student')

    context = {
        "course": course,
        "session_year": session_year,
    }

    return render(request, 'Hod/add_student.html', context)

@admin_required
@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()
    context = {
        "student" : student
    }
    return render(request, 'Hod/view_student.html', context)


@admin_required
@login_required(login_url='/')
def EDIT_STUDENT(request, id):
    student = Student.objects.filter(id=id)
    course = Course.objects.all()
    session_year = Session.objects.all()
    context = {
        "student" : student,
        "course" : course,
        "session_year" : session_year,
    }
    return render(request, 'Hod/edit_student.html', context)


@admin_required
@login_required(login_url='/')
def UPDATE_STUDENT(request):
    try:
        if request.method == "POST":
            student_id = request.POST.get('student_id')
            print(student_id)
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            course_id = request.POST.get('course_id')
            session_year_id = request.POST.get('session_year_id')

            user = CustomUser.objects.get(id = student_id)

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username

            if password != None and password != "":
                user.set_password(password)
            if profile_pic != None and profile_pic != "":
                user.profile_pic = profile_pic
            user.save()

            student = Student.objects.get(admin = student_id)
            student.address = address
            student.gender = gender

            course = Course.objects.get(id = course_id)
            student.course_id = course

            session_year = Session.objects.get(id=session_year_id)
            student.session_year_id=session_year

            student.save()
            messages.success(request,'Student Updated Successfully !')
            return redirect('view_student')
    except:
        messages.warning(request,'All fields are mandatory while updating a student !')

    return render(request,'Hod/edit_student.html')


@admin_required
@login_required(login_url='/')
def DELETE_STUDENT(request, admin):
    student = CustomUser.objects.get(id=admin)
    student.delete()
    messages.success(request, 'Student Deleted Successfully !')

    return redirect('view_student')


@admin_required
@login_required(login_url='/')
def ADD_COURSE(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')

        course = Course(
            name = course_name,
        )
        course.save()
        messages.success(request, 'Course Successfully added !')
        return redirect('add_course')
    return render(request, 'Hod/add_course.html')


@admin_required
@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Course.objects.all()
    context = {
        "course" : course
    }
    return render(request, 'Hod/view_course.html', context)


@admin_required
@login_required(login_url='/')
def EDIT_COURSE(request, id):
    course = Course.objects.filter(id=id)
    context = {
        "course" : course,
    }
    return render(request, 'Hod/edit_course.html', context)


@admin_required
@login_required(login_url='/')
def UPDATE_COURSE(request):
    try:
        if request.method == "POST":
            course_name = request.POST.get('course_name')
            course_id = request.POST.get('course_id')

            course = Course.objects.get(id=course_id)
            course.name= course_name
            course.updated_at = datetime.datetime.now()
            course.save()
            messages.success(request, 'Course details Updated !')
    except:
        messages.warning(request, 'No course is selected to edit!')

    return render(request,'Hod/edit_course.html')


@admin_required
@login_required(login_url='/')
def DELETE_COURSE(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.success(request, 'Course Deleted Successfully !')

    return redirect('view_course')


@admin_required
@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'This Email is already registered !')
            return redirect('add_staff')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'This Username is already registered !')
            return redirect('add_staff')

        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                profile_pic=profile_pic,
                user_type=2,
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin=user,
                address=address,
                gender=gender,
            )
            staff.save()
            messages.success(request, user.first_name + " " + user.last_name + ' Successfully added !')
            return redirect('add_staff')

    return render(request, 'Hod/add_staff.html')


@admin_required
@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context = {
        "staff" : staff,
    }
    return render(request, 'Hod/view_staff.html', context)


@admin_required
@login_required(login_url='/')
def EDIT_STAFF(request, id):
    staff = Staff.objects.filter(id=id)
    context = {
        "staff": staff,
    }
    return render(request, 'Hod/edit_staff.html', context)


@admin_required
@login_required(login_url='/')
def UPDATE_STAFF(request):
    try:
        if request.method == "POST":
            staff_id = request.POST.get('staff_id')
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            address = request.POST.get('address')
            gender = request.POST.get('gender')

            user = CustomUser.objects.get(id = staff_id)

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username

            if password != None and password != "":
                user.set_password(password)
            if profile_pic != None and profile_pic != "":
                user.profile_pic = profile_pic

            user.save()

            staff = Staff.objects.get(admin = staff_id)
            staff.address = address
            staff.gender = gender

            staff.save()
            messages.success(request,'Staff Updated Successfully !')
            return redirect('view_staff')
    except:
        messages.warning(request,'All fields are mandatory while updating a staff !')
    return render(request,'Hod/edit_staff.html')


@admin_required
@login_required(login_url='/')
def DELETE_STAFF(request, admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request, 'Staff Deleted Successfully !')

    return redirect('view_staff')


def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    seen_notification = Staff_Notification.objects.all().order_by('-id')
    context = {
        'staff': staff,
        'seen_notification': seen_notification,
    }
    return render(request, 'Hod/staff_notification.html', context)


def SAVE_STAFF_NOTIFICATION(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin = staff_id)
        notification = Staff_Notification(
            staff_id=staff,
            message=message,
        )
        notification.save()
        messages.success(request, 'Notification Successfully Sent')
        return redirect('staff_send_notification')


    return None
