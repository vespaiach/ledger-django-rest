from typing import List

from ledger_api.models import Reason, Transaction
from ledger_api.selectors import get_reason_by_text
from ledger_core.exception import throw_validation_error
from ledger_core.validators import validate_require


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


def create_transaction(user_id: int, amount: int, date: str, note: str, reasons: List[str]) -> Transaction:
    tx = Transaction(user_id=user_id, amount=amount, date=date, note=note)
    tx.full_clean()

    validate_require("reasons", reasons)

    tx.save()

    return update_transaction_reasons(tx, reasons)


def update_transaction(id: int, user_id: int, **kwargs) -> Transaction:
    tx = Transaction.objects.get(pk=id, user__id=user_id)

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


def delete_transaction(id: int, user_id: int) -> None:
    tx = Transaction.objects.get(pk=id, user__id=user_id)

    tx.reasons.clear()
    tx.delete()
