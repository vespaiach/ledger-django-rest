from django import forms

from ledger_core.exception import throw_validation_error


class BaseForm(forms.Form):
    @property
    def sanitized_data(self):
        if not hasattr(self, 'cleaned_data') or self.cleaned_data is None:
            self.full_clean()

        if self.is_valid():
            return self.cleaned_data
        else:
            throw_validation_error("Input validation fail", self.errors)


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

        if dt['reasons'] is not None:
            dt['reasons'] = dt['reasons'].split(',')

        return dt
