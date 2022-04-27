from functools import wraps
from django.core.exceptions import PermissionDenied


def validate_request(validator_list):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):

            for validator in validator_list:
                validator(request)

            return func(request, *args, **kwargs)

        return inner

    return decorator


def require_token(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.TOKEN is None:
            raise PermissionDenied('Token required')

        return func(request, *args, **kwargs)

    return inner
