import json
from django.forms import ValidationError
from django.http import QueryDict

from ledger_auth.services import decode_token, is_revoked


class JSONContentTypeMiddleware(object):
    """
    Read and convert body that has content-type = application/json to json.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        content_type = request.META.get('CONTENT_TYPE', '').lower()
        method = request.method

        if 'application/json' in content_type and request.body and method != 'GET':
            try:
                q_data = QueryDict('', mutable=True)
                q_data.update(json.loads(request.body))
            except:
                raise ValidationError('Wrong json format')
            else:
                setattr(request, method, q_data)

        response = self.get_response(request)

        return response


class TokenMiddleware(object):
    """
    Read and decode token from authorization header.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def _get_token(self, request):
        authorization = request.META.get('authorization', '')

        if len(authorization) > 0:
            token = authorization if not authorization.startswith(
                'Bearer ') else authorization[6:]

            return token
        return None

    def __call__(self, request):
        request.TOKEN = None

        token = self._get_token(request)

        if token and not is_revoked(token):
            token_dict = decode_token(token)

            if token_dict:
                request.TOKEN = {"payload": token_dict, "token": token}

        response = self.get_response(request)

        return response
