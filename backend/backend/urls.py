from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

from payments.views import create_payout, get_balance_view


def home(request):
    return HttpResponse("Payout API is running")


urlpatterns = [
    path('', home),  # ✅ THIS FIXES YOUR ISSUE
    path('admin/', admin.site.urls),

    path('api/payouts/', create_payout),
    path('api/balance/', get_balance_view),
]