from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator

from ledger_core.exception import throw_validation_error
from ledger_auth.services import generate_token, revoke_token
from ledger_core.views import APIBaseView
from ledger_auth.validations import PostTokenForm


@method_decorator(csrf_exempt, name='dispatch')
class TokenView(APIBaseView):
    def post(self, request):
        token_form = PostTokenForm(request.POST)

        user = authenticate(request, **token_form.sanitized_data)

        if user is None:
            throw_validation_error(
                message='username or password was not correct')

        return dict(token=generate_token(user.id))

    def delete(self, request):
        if request.TOKEN is not None:
            revoke_token(request.TOKEN['token'],
                         request.TOKEN['payload']['exp'])

        return None
