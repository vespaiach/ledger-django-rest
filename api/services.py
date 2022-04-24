from typing import List
from django.conf import settings
from jwt import encode
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.forms import ValidationError
from api.models import Reason, Transaction
from api.selectors import get_reason_by_text


def create_reason(text: str) -> Reason:
    reason = Reason(text=text)
    reason.full_clean()
    reason.save()

    return reason


def update_transaction_reasons(tx: Transaction, reasons: List[str]) -> Transaction:
    for r in reasons:
        if len(r) == 0:
            continue

        reason = get_reason_by_text(r)
        if reason:
            tx.reasons.add(reason)
        else:
            tx.reasons.add(create_reason(r))

    return tx


def create_transaction(amount: int, date: str, note: str, reasons: List[str]) -> Transaction:
    tx = Transaction(amount=amount, date=date, note=note)
    tx.full_clean()

    if len(reasons) == 0:
        raise ValidationError("Please enter reasons.")

    tx.save()

    return update_transaction_reasons(tx, reasons)


def update_transaction(id: int, **kwargs) -> Transaction:
    tx = Transaction.objects.get(pk=id)

    if 'amount' in kwargs:
        tx.amount = kwargs['amount']

    if 'date' in kwargs:
        tx.date = kwargs['date']

    if 'note' in kwargs:
        tx.note = kwargs['note']

    tx.full_clean()
    tx.save()

    if 'reasons' in kwargs:
        reasons = kwargs['reasons'] if type(kwargs['reasons']) is list else [
            kwargs['reasons']]
        tx.reasons.clear()
        return update_transaction_reasons(tx, reasons)


def delete_transaction(id: int) -> None:
    tx = Transaction.objects.get(pk=id)

    tx.reasons.clear()
    tx.delete()
