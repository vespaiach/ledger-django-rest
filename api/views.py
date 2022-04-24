from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from api.models import RevokedToken

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


@csrf_exempt
@require_http_methods(['GET'])
def revoke(request):
    if request.TOKEN is not None:
        RevokedToken.objects.create(token=request.TOKEN['token_str'])
        return JsonResponse({"data": False})

    return JsonResponse({"data": True})
