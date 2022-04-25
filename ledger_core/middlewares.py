from django.conf import settings
from django.forms import ValidationError
from django.http import JsonResponse
import os


class ExceptionHandlerMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if settings.DEBUG and not os.environ.get('TESTING'):
            return None

        if isinstance(exception, ValidationError):
            return JsonResponse(data=dict(message=exception.message, fields=exception.params), status=400)

        return JsonResponse(data=dict(message="Something went wrong"), status=500)
