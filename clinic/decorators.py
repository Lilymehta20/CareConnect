from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(role):
    def decorator(view):
        @login_required
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if request.user.role != role and not request.user.is_superuser:
                raise PermissionDenied
            return view(request, *args, **kwargs)
        return wrapped
    return decorator
