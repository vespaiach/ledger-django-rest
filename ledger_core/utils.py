import json
from functools import wraps
from django.test import TestCase
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
            raise PermissionDenied("Token required")

        return func(request, *args, **kwargs)

    return inner


class APITestCase(TestCase):
    def is_status_200(self, response):
        self.assertEqual(response.status_code, 200)

    def is_status_400(self, response):
        self.assertEqual(response.status_code, 400)

    def is_status_404(self, response):
        self.assertEqual(response.status_code, 404)

    def is_json_content(self, response):
        self.assertEqual(response.headers["Content-Type"], "application/json")

    def to_dict(self, response):
        return json.loads(response.content.decode("utf-8"))
