from django.shortcuts import render
from functools import wraps


def moderator_login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='Accountants').exists():
            return function(request, *args, **kwargs)
        else:
            context = {
                'title': ('403 Forbidden'),
                'message': ('You are not allowed to access this page!')
            }
            # you can also return redirect to another page here.
            return render(request, 'base.html', context)

    return wrap