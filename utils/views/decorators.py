from django.shortcuts import redirect


def login_required_custom(view_func):
    """
    Decorator for views that checks that the admin is logged in.
    """

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('sign_in')

    return wrapper


def admin_required(view_func):
    """
    Decorator for views that checks that the admin is logged in.
    """

    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('meeting:room_list')

    return wrapper


def admin_or_lead_required(view_func):
    """
    Decorator for views that checks that the admin is logged in.
    """

    def wrapper(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_lead:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('meeting:room_list')

    return wrapper
