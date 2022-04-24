from functools import wraps


def validate_request(validator_list):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):

            for validator in validator_list:
                validator(request)

            return func(request, *args, **kwargs)

        return inner

    return decorator
