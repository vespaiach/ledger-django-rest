from django import forms

from ledger_core.validators import BaseForm


class GetTransactionsForm(BaseForm):
    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)

    from_date = forms.DateTimeField(required=False)
    to_date = forms.DateTimeField(required=False)

    from_amount = forms.IntegerField(required=False)
    to_amount = forms.IntegerField(required=False)

    reasons = forms.CharField(max_length=256, required=False)

    @property
    def sanitized_data(self):
        dt = dict(super().sanitized_data)

        if dt['reasons'] is not None and len(dt['reasons']) > 0:
            dt['reasons'] = dt['reasons'].split(',')
        else:
            dt['reasons'] = None

        if not dt['page']:
            dt['page'] = 1

        if not dt['per_page']:
            dt['per_page'] = 50

        return dt


class PostTransactionsForm(BaseForm):
    amount = forms.IntegerField(required=True)
    date = forms.DateTimeField(required=True)
    reasons = forms.JSONField(required=True)
    note = forms.CharField(required=False, max_length=511)

    @property
    def sanitized_data(self):
        return dict(super().sanitized_data)


class PutTransactionsForm(BaseForm):
    id = forms.IntegerField(required=True)
    amount = forms.IntegerField(required=False)
    date = forms.DateTimeField(required=False)
    reasons = forms.JSONField(required=False)
    note = forms.CharField(required=False, max_length=511)

    @property
    def sanitized_data(self):
        return dict(super().sanitized_data)


class OnlyIdTransactionsForm(BaseForm):
    id = forms.IntegerField(required=True, min_value=1)
