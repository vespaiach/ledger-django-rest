from django.core.management.base import BaseCommand

from faker import Faker
from ledger_api.models import Reason, Transaction

fake = Faker()


class Command(BaseCommand):
    help = "Generate dummy data for testing"

    # https://stackoverflow.com/questions/41401202/django-command-throws-typeerror-handle-got-an-unexpected-keyword-argument
    def handle(self, *args, **options):
        self.reasons = []

        for i in range(100):
            self.reasons.append(Reason.objects.create(text=fake.sentence()))

        for i in range(200):
            tx = Transaction(
                amount=fake.pyint(
                    min_value=-100, max_value=100)*100,
                date=fake.date_between(start_date='-2y'),
                note=fake.text(),
            )
            tx.save()

            times = fake.pyint(max_value=3)

            for i in range(times):
                try:
                    tx.reasons.add(self.reasons[fake.pyint(max_value=99)])
                except:
                    print('duplicated')
