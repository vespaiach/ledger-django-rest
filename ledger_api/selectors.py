from typing import List
from django.core.paginator import Paginator

from ledger_api.models import Reason, Transaction


def get_transactions(user_id, page=1, record_per_page=50, **kwargs) -> Paginator:
    """
    Using Paginator is hurting database performance
    Todo: find another way to do pagination
    """
    tx_manager = Transaction.objects
    tx_manager = tx_manager.filter(user__pk=user_id)

    if "from_date" in kwargs:
        tx_manager = tx_manager.filter(
            date__gte=kwargs["from_date"])

    if "to_date" in kwargs:
        tx_manager = tx_manager.filter(
            date__lte=kwargs["to_date"])

    if "from_amount" in kwargs:
        tx_manager = tx_manager.filter(
            amount__gte=kwargs["from_amount"])

    if "to_amount" in kwargs:
        tx_manager = tx_manager.filter(
            amount__lte=kwargs["to_amount"])

    if "reasons" in kwargs:
        reasons = kwargs['reasons'] if type(kwargs['reasons']) is list else [
            kwargs['reasons']]
        tx_manager = tx_manager.filter(reasons__in=reasons)

    paging = Paginator(tx_manager.all(), record_per_page)

    return paging.page(page).object_list, paging.num_pages, paging.count


def get_transaction(id: int, user_id=int) -> Transaction:
    return Transaction.objects.get(pk=id, user__id=user_id)


def get_reason_by_text(text: str) -> Reason:
    try:
        return Reason.objects.get(text__exact=text)
    except:
        return None


def get_reasons() -> List[Reason]:
    return Reason.objects.order_by('text').all()
