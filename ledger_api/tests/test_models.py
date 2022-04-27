from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from ledger_api.models import Reason, Transaction

from ledger_api.selectors import get_reason_by_text, get_transactions
from ledger_api.services import create_reason, create_transaction, delete_transaction, update_transaction


class ReasonServiceTest(TestCase):
    fixtures = ['reason.yaml']

    def test_create_reason_sucess(self):
        reason = create_reason("giftcards")

        self.assertTrue(reason.id == 3)

    def test_duplicated_reason(self):
        with self.assertRaises(ValidationError):
            create_reason("food")

    def test_long_text_reason(self):
        with self.assertRaises(ValidationError):
            create_reason("long text"*100)

    def test_empty_text_reason(self):
        with self.assertRaises(ValidationError):
            create_reason("")


class ReasonSelectorTest(TestCase):
    def test_select_none_existing_reason(self):
        self.assertEqual(get_reason_by_text("random text"), None)


class CreateTransactionTest(TestCase):
    fixtures = ['transaction.yaml']

    def setUp(self):
        self.UserModel = get_user_model()
        self.user = self.UserModel.objects.get(username='tony')
        return super().setUp()

    def test_create_transaction_success(self):
        tx = create_transaction(self.user.id,
                                100, '2022-04-20 00:00:00.000+00:00', 'tips', ['bonus', 'tips'])

        self.assertEqual(tx.id, 2)

        bonus = get_reason_by_text('bonus')
        tips = get_reason_by_text('tips')

        self.assertTrue(bonus.id > 0)
        self.assertTrue(tips.id > 0)

        self.assertTrue(any(tx.id == 2 for tx in bonus.transaction_set.all()))
        self.assertTrue(any(tx.id == 2 for tx in tips.transaction_set.all()))

    def test_create_transaction_missing_reason(self):
        with self.assertRaises(ValidationError):
            create_transaction(self.user.id,
                               amount=100, date='2022-04-20 00:00:00.00000 +00:00', note='tips', reasons=[])

    def test_create_too_long_note_transaction(self):
        with self.assertRaises(ValidationError):
            create_transaction(self.user.id,
                               amount=100, date='2022-04-20 00:00:00.00000 +00:00', note='too long text'*200, reasons=['test'])

    def test_create_transaction_invalid_user_id(self):
        with self.assertRaises(ValidationError):
            create_transaction(3,
                               amount=100, date='2022-04-20 00:00:00.00000 +00:00', note='too long text'*200, reasons=['test'])


class UpdateTransactionTest(TestCase):
    fixtures = ['transaction.yaml']

    def test_update_transaction_success(self):
        update_transaction(id=1, user_id=1,
                           amount=70000, date='2022-04-21 00:00:00.000+00:00', note='paychecks', reasons=['compensate'])

        tx = Transaction.objects.get(pk=1)

        self.assertEqual(tx.id, 1)
        self.assertEqual(tx.amount, 70000)
        self.assertEqual(tx.note, 'paychecks')

        reasons = tx.reasons.all()

        self.assertEqual(len(reasons), 1)
        self.assertEqual(reasons[0].text, 'compensate')
        self.assertEqual(tx.date, datetime.fromisoformat(
            '2022-04-21 00:00:00.000+00:00'))

    def test_update_none_exist_transaction(self):
        with self.assertRaises(ObjectDoesNotExist):
            update_transaction(-1, user_id=-1, amount=70000,
                               date='2022-04-21 00:00:00.000+00:00', note='paychecks', reasons=['compensate'])


class DeleteTransactionTest(TestCase):
    fixtures = ['transaction.yaml']

    def test_delete_transaction_success(self):
        delete_transaction(1, 1)

        with self.assertRaises(ObjectDoesNotExist):
            Transaction.objects.get(pk=1)

        trans = Reason.objects.get(pk=1).transaction_set.all()

        self.assertEqual(len(trans), 0)


class QueryTransactionTest(TestCase):
    fixtures = ['tx_query.yaml']

    def test_query_transaction_by_date(self):
        transactions, total_page, total_record = get_transactions(user_id=1,
                                                                  from_date='2022-04-20 00:00:00.000+00:00', to_date='2022-04-23 00:00:00+00:00')

        self.assertEqual(len(transactions), 2)
        self.assertEqual(total_page, 1)
        self.assertEqual(total_record, 2)

    def test_query_income_transaction(self):
        transactions, total_page, total_record = get_transactions(user_id=1,
                                                                  from_amount=0)

        self.assertEqual(len(transactions), 2)
        self.assertEqual(total_page, 1)
        self.assertEqual(total_record, 2)

    def test_query_expense_transaction(self):
        transactions, total_page, total_record = get_transactions(user_id=1,
                                                                  to_amount=0)

        self.assertEqual(len(transactions), 3)
        self.assertEqual(total_page, 1)
        self.assertEqual(total_record, 3)

    def test_query_transaction_by_single_reason(self):
        transactions, total_page, total_record = get_transactions(user_id=1,
                                                                  reasons=['salary'])

        self.assertEqual(len(transactions), 1)
        self.assertEqual(total_page, 1)
        self.assertEqual(total_record, 1)
