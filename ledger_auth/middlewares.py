import json
from django.http import QueryDict

from ledger_core.exception import throw_validation_error
from ledger_auth.services import decode_token, is_revoked


class JSONContentTypeMiddleware(object):
    """
    Read and convert body that has content-type = application/json to json.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        content_type = request.META.get("CONTENT_TYPE", "").lower()
        method = request.method

        # GET, DELETE and HEAD have no request body defined semantics as per RFC 7231.
        except_methods = ["GET", "DELETE", "HEAD"]
        if "application/json" in content_type and request.body and method not in except_methods:
            try:
                q_data = QueryDict("", mutable=True)
                q_data.update(json.loads(request.body))
            except Exception:
                throw_validation_error(message="Payload had wrong json format")
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
        authorization = request.META.get("HTTP_AUTHORIZATION", "")

        if len(authorization) > 0:
            token = authorization if not authorization.startswith("Bearer ") else authorization[7:]

            return token
        return None

    def __call__(self, request):
        request.TOKEN = None

        token = self._get_token(request)

        try:
            if token and not is_revoked(token):
                token_dict = decode_token(token)

                if token_dict:
                    request.TOKEN = {"payload": token_dict, "token": token}
        except Exception:
            request.TOKEN = None

        response = self.get_response(request)

        return response
