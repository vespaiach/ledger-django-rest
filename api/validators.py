from functools import wraps
from django import forms


def check_token_input(request):
    class TokenForm(forms.Form):
        username = forms.CharField(max_length=64, required=True)
        password = forms.CharField(max_length=64, required=True)

    token_form = TokenForm(request.POST)
    if not token_form.is_valid():
        raise forms.ValidationError('Username and password are required.')

    request.cleaned_data = request.cleaned_data if 'cleaned_data' in request and request.cleaned_data is not None else {}
    request.cleaned_data.update(token_form.cleaned_data)


def validate_request(validator_list):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):

            for validator in validator_list:
                validator(request)

            return func(request, *args, **kwargs)

        return inner

    return decorator
