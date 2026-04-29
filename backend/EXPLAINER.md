# Payout System Backend - Explainer

## Overview
This project implements a payout system where merchants can transfer money to bank accounts safely. The system ensures consistency using a ledger-based balance model and prevents duplicate transactions using idempotency.

---

## Core Features

### 1. Create Payout API
POST /api/payouts/

- Validates merchant and bank account
- Checks available balance before processing
- Deducts amount via ledger entry
- Uses idempotency key to prevent duplicate payouts

---

### 2. Balance API
GET /api/balance/?merchant_id=ID

- Returns current balance
- Balance is calculated dynamically from ledger entries

---

## Idempotency Design

Each payout request includes an `idempotency_key`.

- Same key → same response returned
- No duplicate payout created
- Enforced at database level using unique constraint

This ensures safe retries in real-world systems.

---

## Ledger-Based Balance System

Instead of storing balance directly, we use a ledger.

- `credit` → adds funds
- `debit` → subtracts funds

### Formula:
Balance = Total Credits - Total Debits

This approach avoids inconsistencies and supports auditability.

---

## Error Handling

### Duplicate Request
Returns existing payout instead of creating a new one.

### Insufficient Balance
Rejects payout if funds are not enough.

---

## Live API

https://playto-payout-sdxw.onrender.com/

---

## Test Data

merchant_id: d63498b8-4eb1-4293-ac0e-8089ab73d4a5  
bank_account_id: 4b551efb-35b2-4e39-965a-dec0c69d824c  

---

## Example Request

POST /api/payouts/

{
  "merchant_id": "d63498b8-4eb1-4293-ac0e-8089ab73d4a5",
  "bank_account_id": "4b551efb-35b2-4e39-965a-dec0c69d824c",
  "amount_paise": 5000,
  "idempotency_key": "test_1"
}

---

## Key Design Decisions

- Used ledger instead of direct balance storage for consistency
- Used idempotency keys to prevent duplicate payouts
- Kept APIs minimal and focused as per requirements

---

## Conclusion

The system ensures:
- Safe transactions
- No duplicate payouts
- Accurate balance tracking
- Clean and simple API design