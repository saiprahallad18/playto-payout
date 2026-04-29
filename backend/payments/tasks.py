import time
import random
from .models import Payout, LedgerEntry

def process_payout(payout_id):
    payout = Payout.objects.get(id=payout_id)
    merchant = payout.merchant

    # STEP 1: mark processing
    payout.status = "processing"
    payout.save()

    time.sleep(2)

    # STEP 2: simulate success/failure
    if random.choice([True, False]):
        # ❌ FAILURE
        payout.status = "failed"
        payout.save()

        # 🔁 REFUND ENTRY
        LedgerEntry.objects.create(
            merchant=merchant,
            entry_type='credit',
            amount_paise=payout.amount_paise,
            description='Refund for failed payout'
        )

        print("❌ FAILED + REFUND DONE")
        return

    # ✅ SUCCESS
    payout.status = "completed"
    payout.save()

    print("✅ COMPLETED")