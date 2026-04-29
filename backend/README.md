# Payout System Backend

## Live API

https://playto-payout-sdxw.onrender.com/

---

## Test Data

merchant_id: d63498b8-4eb1-4293-ac0e-8089ab73d4a5  
bank_account_id: 4b551efb-35b2-4e39-965a-dec0c69d824c  

---

## Check Balance

GET  
https://playto-payout-sdxw.onrender.com/api/balance/?merchant_id=d63498b8-4eb1-4293-ac0e-8089ab73d4a5

---

## Create Payout

POST  
https://playto-payout-sdxw.onrender.com/api/payouts/

Body:
{
  "merchant_id": "d63498b8-4eb1-4293-ac0e-8089ab73d4a5",
  "bank_account_id": "4b551efb-35b2-4e39-965a-dec0c69d824c",
  "amount_paise": 5000,
  "idempotency_key": "test_1"
}

---

## Features

- Create payout API  
- Idempotency support  
- Ledger-based balance system  
- Balance API  

---

## Tech Stack

- Django  
- Django REST Framework  
- SQLite (dev) / Postgres (Render)

---

## Notes

- Same idempotency key → duplicate request blocked  
- Balance updates after payout  

