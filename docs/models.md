# Models

::: django_util.models

## Relation

| source       | relation | target            |
| ------------ | -------- | ----------------- |
| User         | 1-n      | Payment Method    |
| User         | 1-n      | Subscription      |
| Plan         | 1-n      | Subscription      |
| Coupon       | n-n      | Subscription      |
| Subscription | 1-n      | Transaction       |
| Transaction  | 1-n      | Transaction Event |

## Payment vs Transaction

| Feature  | Payment                           | Transaction                                          |
| -------- | --------------------------------- | ---------------------------------------------------- |
| Focus    | Exchange of value                 | Record of exchange                                   |
| Scope    | Narrower (specific exchange)      | Broader (includes payment, but also other exchanges) |
| Examples | Cash, credit card, digital wallet | Purchase, sale, refund, transfer                     |

A payment is the action of exchanging value, while a transaction is the record of that action and its associated details.

## transaction.state vs transaction_event.choice_type

`transactions.state`

- Represents the overall state of the transaction.
- Provides a high-level summary of the transaction's lifecycle.
- Typically has a limited set of values (e.g., pending, completed, failed, canceled).
- Is relatively static once set, although it might be updated in specific circumstances (e.g., from pending to failed).

`transaction_event.choice_type`

- Records specific actions or changes that occur during the transaction's lifecycle.
- Provides a detailed history of the transaction's progression.
- Can have a wider range of values (e.g., created, authorized, captured, refunded, disputed).
- Represents dynamic events that can occur multiple times for a single transaction.

Think of `transactions.state` as a snapshot of the transaction's current state, while `transaction_event.choice_type` is a record of the individual steps taken to reach that state.

**Example**

A transaction's state might be "completed".
The `transaction_event` for that transaction might include events like "created", "authorized", and "captured".

## transaction.amount vs plan.price vs subscription.prorated_amount vs coupon.discount_value

| Field                          | Description                                              |
| ------------------------------ | -------------------------------------------------------- |
| `transaction.amount`           | Actual amount charged or refunded for a transaction      |
| `plan.price`                   | Base price of a subscription plan                        |
| `subscription.prorated_amount` | Adjusted amount for a subscription change                |
| `coupon.discount_value`        | Amount or percentage of the discount offered by a coupon |

**Example**

A user has a subscription with a `plan.price` of $100.

They use a coupon with a discount_value of 20%.

The discount amount is calculated as $100 x 20% = $20.

The `transaction.amount` becomes $100 - $20 = $80.

If the user upgrades to a plan with a `plan.price` of $150 mid-month, a `subscription.prorated_amount` of $75 might be calculated for the remaining half of the month, and the `transaction.amount` for the upgrade would be $150 + $75 = $225.
