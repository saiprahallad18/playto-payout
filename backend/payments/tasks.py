from celery import shared_task
from django.utils import timezone
import time

from .models import Payout


@shared_task(bind=True, max_retries=3)
def process_payout(self, payout_id):
    try:
        payout = Payout.objects.get(id=payout_id)

        payout.status = 'processing'
        payout.processing_started_at = timezone.now()
        payout.save()

        # simulate processing delay
        time.sleep(5)

        # simulate success
        payout.status = 'completed'
        payout.save()

    except Exception as e:
        raise self.retry(exc=e, countdown=5)