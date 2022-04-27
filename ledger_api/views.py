from django.utils.decorators import method_decorator

from ledger_api.selectors import get_reasons, get_transaction, get_transactions
from ledger_api.validations import GetTransactionsForm
from ledger_core.utils import require_token
from ledger_core.views import APIBaseView


class ReasonView(APIBaseView):
    def get(self, request):
        return get_reasons()


@method_decorator(require_token, name='dispatch')
class TransactionView(APIBaseView):
    def get(self, request, id):
        return get_transaction(id, request.TOKEN['payload']['user_id'])


@method_decorator(require_token, name='dispatch')
class TransactionsView(APIBaseView):
    def get(self, request):
        user_id = request.TOKEN['payload']['user_id']
        data = request.GET.dict()

        form = GetTransactionsForm(request.GET)

        return get_transactions(user_id=user_id, **form.sanitized_data)
