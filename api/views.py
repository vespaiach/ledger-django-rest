from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from api.validators import check_token_input, validate_request
from api.services import exchange_for_token


@csrf_exempt
@require_http_methods(['POST'])
@validate_request([check_token_input])
def token(request):
    token = exchange_for_token(
        request, username=request.cleaned_data['username'], password=request.cleaned_data['password'])

    if token is None:
        raise ValidationError('username or password was not correct')

    return JsonResponse({"token": token})
