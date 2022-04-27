from django import forms

from ledger_core.validators import BaseForm


class PostTokenForm(BaseForm):
    username = forms.CharField(max_length=64, required=True)
    password = forms.CharField(max_length=64, required=True)
