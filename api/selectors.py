from typing import List
from django.core.paginator import Paginator
from api.models import Reason, Transaction
from django.core.exceptions import ObjectDoesNotExist


def get_transactions(page=1, record_per_page=50, **kwargs) -> Paginator:
    """Using Paginator is hurting database performance
       Todo: find another way to do pagination
    """
    tx_manager = Transaction.objects

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


def get_transaction(id: int) -> Transaction:
    return Transaction.objects.get(pk=id)


def get_reason_by_text(text: str) -> Reason:
    try:
        return Reason.objects.get(text__exact=text)
    except ObjectDoesNotExist:
        return None


def get_reasons() -> List[Reason]:
    return Reason.objects.order_by('text').all()
