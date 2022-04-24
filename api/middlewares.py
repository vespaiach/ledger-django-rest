from functools import lru_cache
import json
from django.conf import settings
import jwt
from django.http import QueryDict

from api.models import RevokedToken


class JSONMiddleware(object):
    """
    Read body and convert to dict
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'CONTENT_TYPE' in request.META and 'application/json' in request.META['CONTENT_TYPE'] and request.method == 'POST':
            q_data = QueryDict('', mutable=True)
            q_data.update(json.loads(request.body))

            request.POST = q_data

        response = self.get_response(request)

        return response


class TokenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def _get_token(self, request):
        if 'CONTENT_TYPE' in request.META and 'authorization' in request.META['CONTENT_TYPE'] \
            and request.META['CONTENT_TYPE']['authorization'] is not None \
                and len(request.META['CONTENT_TYPE']['authorization']) > 0:

            token = request.META['CONTENT_TYPE']['authorization']
            token = token if not token.startswith(
                'Bearer ') else token[6:]

            return token
        return None

    def _decode_token(self, token):
        try:
            token_dict = jwt.decode(
                token, settings.SECRET_KEY, issuer=settings.JWT_ISSUER, algorithms=[settings.JWT_ALGORITHM])
            return token_dict
        except:
            return None

    @lru_cache(maxsize=20)
    def _is_revoked(self, token):
        try:
            RevokedToken.objects.get(pk=token)
            return True
        except:
            return False

    def __call__(self, request):
        request.TOKEN = None

        token = self._get_token(request)

        if token and not self._is_revoked(token):
            token_dict = self._decode_token(token)

            if token_dict:
                request.TOKEN = token_dict
                request.TOKEN['token_str'] = token

        response = self.get_response(request)

        return response
