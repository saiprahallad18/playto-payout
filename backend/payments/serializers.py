from rest_framework import serializers
from .models import Payout

class PayoutCreateSerializer(serializers.Serializer):
    merchant_id = serializers.UUIDField()
    bank_account_id = serializers.UUIDField()
    amount_paise = serializers.IntegerField()
    idempotency_key = serializers.CharField(max_length=255)