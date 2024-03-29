from django.core.exceptions import ValidationError, PermissionDenied
from django.http import JsonResponse


class ExceptionHandlerMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # if settings.DEBUG and not os.environ.get('TESTING'):
        #     return None

        if isinstance(exception, ValidationError):
            return JsonResponse(data=dict(message=exception.message, fields=exception.params), status=400)

        if isinstance(exception, PermissionDenied):
            return JsonResponse(data=dict(message=str(exception)), status=403)

        return JsonResponse(data=dict(message="Something went wrong"), status=500)
