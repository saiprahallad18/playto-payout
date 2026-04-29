from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

from .models import Merchant, BankAccount, LedgerEntry, Payout
from .serializers import PayoutCreateSerializer
from .tasks import process_payout  


@api_view(['POST'])
def create_payout(request):
    serializer = PayoutCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    data = serializer.validated_data

    merchant = Merchant.objects.get(id=data['merchant_id'])

    # Idempotency check
    existing = Payout.objects.filter(
        merchant=merchant,
        idempotency_key=data['idempotency_key']
    ).first()

    if existing:
        return Response({
            "message": "Duplicate request",
            "payout_id": str(existing.id),
            "status": existing.status
        })

    # Calculate balance
    credits = LedgerEntry.objects.filter(
        merchant=merchant,
        entry_type='credit'
    ).aggregate(total=Sum('amount_paise'))['total'] or 0

    debits = LedgerEntry.objects.filter(
        merchant=merchant,
        entry_type='debit'
    ).aggregate(total=Sum('amount_paise'))['total'] or 0

    balance = credits - debits

    if balance < data['amount_paise']:
        return Response({
            "error": "Insufficient balance"
        }, status=400)

    bank_account = BankAccount.objects.get(id=data['bank_account_id'])

    # ✅ CREATE PAYOUT
    payout = Payout.objects.create(
        merchant=merchant,
        bank_account=bank_account,
        amount_paise=data['amount_paise'],
        idempotency_key=data['idempotency_key']
    )

    # ✅ CREATE LEDGER DEBIT
    LedgerEntry.objects.create(
        merchant=merchant,
        entry_type='debit',
        amount_paise=data['amount_paise'],
        description='Payout'
    )
    process_payout.delay(payout.id)

    return Response({
        "payout_id": str(payout.id),
        "status": payout.status
    }, status=201)