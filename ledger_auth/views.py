from django import forms
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from core.exception import throw_validation_error

from ledger_auth.services import generate_token, revoke_token


@csrf_exempt
@require_http_methods(['POST'])
def token(request):
    class TokenForm(forms.Form):
        username = forms.CharField(max_length=64, required=True)
        password = forms.CharField(max_length=64, required=True)

    token_form = TokenForm(request.POST)
    if not token_form.is_valid():
        raise throw_validation_error(
            message='Username and password are required', extra=token_form.errors)

    user = authenticate(
        request, username=token_form.cleaned_data['username'], password=token_form.cleaned_data['password'])

    if user is None:
        raise throw_validation_error(
            message='username or password was not correct')

    return JsonResponse({"token": generate_token(user.id)})


@csrf_exempt
@require_http_methods(['POST'])
def revoke(request):
    if request.TOKEN is not None:
        revoke_token(request.TOKEN['token'], request.TOKEN['payload']['exp'])
        return JsonResponse({"data": True})

    return JsonResponse({"data": False})
