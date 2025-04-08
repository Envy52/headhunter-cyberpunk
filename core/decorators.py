from django.shortcuts import redirect
from functools import wraps


def fixer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'fixer':
            return view_func(request, *args, **kwargs)
        return redirect('home')

    return _wrapped_view


def mercenary_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'mercenary':
            return view_func(request, *args, **kwargs)
        return redirect('home')

    return _wrapped_view
