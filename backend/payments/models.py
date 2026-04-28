from django.db import models
from django.utils import timezone
import uuid


class Merchant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LedgerEntry(models.Model):
    CREDIT = 'credit'
    DEBIT = 'debit'
    ENTRY_TYPES = [(CREDIT, 'Credit'), (DEBIT, 'Debit')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='ledger_entries')
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES)
    amount_paise = models.BigIntegerField()
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.merchant.name} - {self.entry_type} - {self.amount_paise}"


class BankAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='bank_accounts')
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=11)
    account_holder_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.merchant.name} - {self.account_number}"


class Payout(models.Model):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='payouts')
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount_paise = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    idempotency_key = models.CharField(max_length=255)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processing_started_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('merchant', 'idempotency_key')

    def __str__(self):
        return f"{self.merchant.name} - {self.amount_paise} - {self.status}"


class IdempotencyRecord(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    response_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('merchant', 'key')