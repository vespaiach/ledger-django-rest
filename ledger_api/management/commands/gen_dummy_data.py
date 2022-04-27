import pytz
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import datetime

from faker import Faker
from ledger_api.services import create_transaction

fake = Faker()


UserModel = get_user_model()


EXPENSE_REASONS = ['food', 'fuel', 'medicine', 'gas', 'water', 'electricity']
INCOME_REASONS = ['salary', 'tips', 'bonus']


class Command(BaseCommand):
    help = "Generate dummy data for testing"

    # https://stackoverflow.com/questions/41401202/django-command-throws-typeerror-handle-got-an-unexpected-keyword-argument
    def handle(self, *args, **options):
        try:
            user = UserModel.objects.get(username="tester")
        except:
            user = UserModel.objects.create_user(
                username="tester", password="123", email="test@test.com")

        for i in range(100):
            amount = fake.pyint(min_value=-100, max_value=100)*100
            if amount > 0:
                reasons = INCOME_REASONS[fake.pyint(min_value=0, max_value=2)]
            else:
                reasons = EXPENSE_REASONS[fake.pyint(min_value=0, max_value=2)]

            date = fake.date_time_between(start_date='-2y')

            create_transaction(user_id=user.id,
                               date=datetime(date.year, date.month, date.day, date.hour,
                                             date.minute, date.second, 0, pytz.UTC),
                               amount=amount,
                               note=fake.text(),
                               reasons=reasons)

        print('Done!')
