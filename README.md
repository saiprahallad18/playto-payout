# Playto Payout System

## Overview

This project implements a payout processing system for merchants. It allows merchants to initiate payouts, validates available balance using a ledger-based system, prevents duplicate transactions using idempotency, and processes payouts asynchronously using Celery.

---

## Features

* Merchant and bank account management
* Ledger-based balance tracking (credits & debits)
* Payout creation API
* Idempotency handling to prevent duplicate payouts
* Asynchronous payout processing using Celery
* Status lifecycle: pending → processing → completed

---

## Tech Stack

* Django
* Django REST Framework
* PostgreSQL
* Celery
* Redis (Memurai for Windows)

---

## API Endpoint

### Create Payout

**POST** `/api/payouts/`

#### Request Body

```json
{
  "merchant_id": "UUID",
  "bank_account_id": "UUID",
  "amount_paise": 10000,
  "idempotency_key": "payout_001"
}
```

#### Response

```json
{
  "payout_id": "UUID",
  "status": "pending"
}
```

---

## How It Works

1. Validate request input
2. Check idempotency key to prevent duplicates
3. Calculate merchant balance from ledger entries
4. Create payout with status `pending`
5. Trigger Celery background task
6. Worker processes payout and updates status to `completed`

---

## Running the Project

### Start Django Server

```bash
python manage.py runserver
```

### Start Celery Worker (Windows)

```bash
celery -A backend worker --pool=solo -l info
```

---

## Notes

* Pending payouts created before Celery startup will not be processed
* New payouts are handled asynchronously after worker starts

---

## Summary

This system demonstrates a production-style backend architecture with proper handling of financial transactions, ensuring consistency, fault tolerance, and scalability.
# Playto Payout System

## Overview

This project implements a payout processing system for merchants. It allows merchants to initiate payouts, validates available balance using a ledger-based system, prevents duplicate transactions using idempotency, and processes payouts asynchronously using Celery.

---

## Features

* Merchant and bank account management
* Ledger-based balance tracking (credits & debits)
* Payout creation API
* Idempotency handling to prevent duplicate payouts
* Asynchronous payout processing using Celery
* Status lifecycle: pending → processing → completed

---

## Tech Stack

* Django
* Django REST Framework
* PostgreSQL
* Celery
* Redis (Memurai for Windows)

---

## API Endpoint

### Create Payout

**POST** `/api/payouts/`

#### Request Body

```json
{
  "merchant_id": "UUID",
  "bank_account_id": "UUID",
  "amount_paise": 10000,
  "idempotency_key": "payout_001"
}
```

#### Response

```json
{
  "payout_id": "UUID",
  "status": "pending"
}
```

---

## How It Works

1. Validate request input
2. Check idempotency key to prevent duplicates
3. Calculate merchant balance from ledger entries
4. Create payout with status `pending`
5. Trigger Celery background task
6. Worker processes payout and updates status to `completed`

---

## Running the Project

### Start Django Server

```bash
python manage.py runserver
```

### Start Celery Worker (Windows)

```bash
celery -A backend worker --pool=solo -l info
```

---

## Notes

* Pending payouts created before Celery startup will not be processed
* New payouts are handled asynchronously after worker starts

---

## Summary

This system demonstrates a production-style backend architecture with proper handling of financial transactions, ensuring consistency, fault tolerance, and scalability.
