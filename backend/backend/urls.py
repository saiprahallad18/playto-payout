from django.contrib import admin
from django.urls import path
from payments.views import create_payout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/payouts/', create_payout),
]