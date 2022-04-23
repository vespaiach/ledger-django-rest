import json

from django.http import QueryDict


class JSONMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'application/json' in request.META['CONTENT_TYPE'] and request.method == 'POST':
            q_data = QueryDict('', mutable=True)
            q_data.update(json.loads(request.body))

            request.POST = q_data

        response = self.get_response(request)

        return response
