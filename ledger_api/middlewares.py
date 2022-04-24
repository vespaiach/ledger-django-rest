from django.conf import settings
from django.forms import ValidationError as FormValidationError
from django.core.exceptions import ValidationError as CoreValidationError
from django.http import JsonResponse
import os

from core.exception import AppValidationError


class ExceptionHandlerMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if settings.DEBUG and not os.environ.get('TESTING'):
            return None

        if isinstance(exception, AppValidationError):
            return JsonResponse(data=exception.__dict__, status=400)
        elif isinstance(exception, FormValidationError) or isinstance(exception, CoreValidationError):
            return JsonResponse(data=dict(message="Something went wrong", extra=exception.message_dict), status=400)

        return JsonResponse(data=dict(message="Something went wrong"), status=500)
