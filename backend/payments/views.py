from django.db.models import Sum
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Payout, Merchant, BankAccount, LedgerEntry


# -------------------------------
# Helper: Calculate Balance
# -------------------------------
def get_balance(merchant):
    credits = LedgerEntry.objects.filter(
        merchant=merchant,
        entry_type='credit'
    ).aggregate(total=Sum('amount_paise'))['total'] or 0

    debits = LedgerEntry.objects.filter(
        merchant=merchant,
        entry_type='debit'
    ).aggregate(total=Sum('amount_paise'))['total'] or 0

    return credits - debits


# -------------------------------
# GET BALANCE API
# -------------------------------
@api_view(['GET'])
def get_balance_view(request):
    merchant_id = request.GET.get('merchant_id')

    if not merchant_id:
        return Response({"error": "merchant_id is required"}, status=400)

    try:
        merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
        return Response({"error": "Merchant not found"}, status=404)

    balance = get_balance(merchant)

    return Response({
        "merchant_id": str(merchant.id),
        "balance_paise": balance
    })


# -------------------------------
# CREATE PAYOUT API
# -------------------------------
@api_view(['POST'])
def create_payout(request):
    data = request.data

    merchant_id = data.get('merchant_id')
    bank_account_id = data.get('bank_account_id')
    amount_paise = data.get('amount_paise')
    idempotency_key = data.get('idempotency_key')

    # -------------------------------
    # Validation
    # -------------------------------
    if not all([merchant_id, bank_account_id, amount_paise, idempotency_key]):
        return Response({"error": "Missing required fields"}, status=400)

    try:
        amount_paise = int(amount_paise)
    except:
        return Response({"error": "amount_paise must be integer"}, status=400)

    # -------------------------------
    # Fetch merchant
    # -------------------------------
    try:
        merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
        return Response({"error": "Merchant not found"}, status=404)

    # -------------------------------
    # Fetch bank account
    # -------------------------------
    try:
        bank_account = BankAccount.objects.get(id=bank_account_id, merchant=merchant)
    except BankAccount.DoesNotExist:
        return Response({"error": "Bank account not found"}, status=404)

    # -------------------------------
    # Idempotency check (CORRECT)
    # -------------------------------
    existing = Payout.objects.filter(
        merchant=merchant,
        idempotency_key=idempotency_key
    ).first()

    if existing:
        return Response({
            "message": "Duplicate request",
            "payout_id": str(existing.id),
            "status": existing.status
        })

    # -------------------------------
    # Balance check
    # -------------------------------
    balance = get_balance(merchant)

    if amount_paise > balance:
        return Response({"error": "Insufficient balance"}, status=400)

    # -------------------------------
    # Create payout (HANDLE DB ERROR)
    # -------------------------------
    try:
        payout = Payout.objects.create(
            merchant=merchant,
            bank_account=bank_account,
            amount_paise=amount_paise,
            status='success',
            idempotency_key=idempotency_key
        )
    except IntegrityError:
        # fallback for duplicate insert
        existing = Payout.objects.get(
            merchant=merchant,
            idempotency_key=idempotency_key
        )
        return Response({
            "message": "Duplicate request",
            "payout_id": str(existing.id),
            "status": existing.status
        })

    # -------------------------------
    # Ledger entry (debit)
    # -------------------------------
    LedgerEntry.objects.create(
        merchant=merchant,
        entry_type='debit',
        amount_paise=amount_paise,
        description='Payout'
    )

    return Response({
        "payout_id": str(payout.id),
        "status": payout.status
    })