from django import forms
from django.core.exceptions import ValidationError

from ledger_core.exception import throw_validation_error


def validate_require(field_name, val):
    if val is None or len(val) == 0:
        params = {}
        params[field_name] = f"{field_name} is empty or None"
        raise ValidationError("%(field)s is required", params=params)


class BaseForm(forms.Form):
    @property
    def sanitized_data(self):
        if not hasattr(self, "cleaned_data") or self.cleaned_data is None:
            self.full_clean()

        if self.is_valid():
            return self.cleaned_data
        else:
            throw_validation_error("Input validation fail", self.errors)
