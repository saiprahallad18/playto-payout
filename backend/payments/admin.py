from django.contrib import admin
from .models import Merchant, LedgerEntry, BankAccount, Payout, IdempotencyRecord

admin.site.register(Merchant)
admin.site.register(LedgerEntry)
admin.site.register(BankAccount)
admin.site.register(Payout)
admin.site.register(IdempotencyRecord)