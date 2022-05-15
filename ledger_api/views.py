from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from ledger_api.selectors import get_reasons, get_transaction, get_transactions
from ledger_api.services import create_transaction, delete_transaction, update_transaction
from ledger_api.validations import (
    GetTransactionsForm,
    OnlyIdTransactionsForm,
    PostTransactionsForm,
    PutTransactionsForm,
)
from ledger_core.utils import require_token
from ledger_core.views import APIBaseView


class ReasonView(APIBaseView):
    def get(self, request):
        return get_reasons()


@method_decorator(require_token, name="dispatch")
@method_decorator(csrf_exempt, name="dispatch")
class TransactionView(APIBaseView):
    def get(self, request, id):
        user_id = request.TOKEN["payload"]["user_id"]

        form = OnlyIdTransactionsForm({"id": id})

        return get_transaction(user_id=user_id, **form.sanitized_data)

    def delete(self, request, id):
        user_id = request.TOKEN["payload"]["user_id"]

        form = OnlyIdTransactionsForm({"id": id})

        return delete_transaction(user_id=user_id, **form.sanitized_data)


@method_decorator(require_token, name="dispatch")
@method_decorator(csrf_exempt, name="dispatch")
class TransactionsView(APIBaseView):
    def get(self, request):
        user_id = request.TOKEN["payload"]["user_id"]

        form = GetTransactionsForm(request.GET, initial={"page": 1, "per_page": 50})

        result = get_transactions(user_id=user_id, **form.sanitized_data)
        return dict(data=result[0], total_page=result[1], total_record=result[2])

    def post(self, request):
        user_id = request.TOKEN["payload"]["user_id"]
        form = PostTransactionsForm(request.POST)

        return create_transaction(user_id=user_id, **form.sanitized_data)

    def put(self, request):
        user_id = request.TOKEN["payload"]["user_id"]
        form = PutTransactionsForm(request.PUT)

        return update_transaction(user_id=user_id, **form.sanitized_data)


def api_doc(request):
    return HttpResponse(render_to_string("ledger_api/doc.html"))
