from functools import wraps

from django.http import HttpResponse
from django.shortcuts import redirect, render


def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '3':
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'templates/error_404.html')  # Redirect to an access denied page or login page

    return _wrapped_view


def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '2':
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'templates/error_404.html')

    return _wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == '1':
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'error_404.html')
            # return HttpResponse('Access denied..!!')

    return _wrapped_view
