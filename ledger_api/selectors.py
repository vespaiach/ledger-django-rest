from typing import List
from django.core.paginator import Paginator

from ledger_api.models import Reason, Transaction


def get_transactions(
    user_id, page=1, per_page=50, from_date=None, to_date=None, from_amount=None, to_amount=None, reasons=None
):
    """
    Using Paginator is hurting database performance
    Todo: find another way to do pagination
    """
    tx_manager = Transaction.objects
    tx_manager = tx_manager.filter(user__pk=user_id)

    if from_date:
        tx_manager = tx_manager.filter(date__gte=from_date)

    if to_date:
        tx_manager = tx_manager.filter(date__lte=to_date)

    if from_amount is not None:
        tx_manager = tx_manager.filter(amount__gte=from_amount)

    if to_amount is not None:
        tx_manager = tx_manager.filter(amount__lte=to_amount)

    if reasons:
        tx_manager = tx_manager.filter(reasons__in=Reason.objects.filter(text__in=reasons))

    paging = Paginator(tx_manager.all().prefetch_related("reasons"), per_page)

    if paging.count == 0:
        return [], 0, 0

    if page > paging.num_pages:
        return [], paging.num_pages, paging.count

    return paging.page(page).object_list, paging.num_pages, paging.count


def get_transaction(id: int, user_id=int) -> Transaction:
    return Transaction.objects.get(pk=id, user__id=user_id)


def get_reason_by_text(text: str) -> Reason:
    try:
        return Reason.objects.get(text__exact=text)
    except Exception:
        return None


def get_reasons() -> List[Reason]:
    return Reason.objects.order_by("text").all()
