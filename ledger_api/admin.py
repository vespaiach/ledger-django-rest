from django.contrib import admin

from ledger_api.models import Reason, Transaction

# Register your models here.

admin.site.register(Reason)
admin.site.register(Transaction)
