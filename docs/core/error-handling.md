# Error Handling

`syntiq-mt5` never raises exceptions for operational failures. All errors are returned as `Result` values.

---

## How MT5 errors work

The raw `MetaTrader5` library stores the last error in global state. After every call you must manually call `mt5.last_error()` to retrieve it — and if you forget, the error is lost.

`syntiq-mt5` captures `last_error()` immediately after every operation and attaches it to the returned `Result`. You never need to call `last_error()` yourself.

---

## Reading errors

```python
res = mt5.login(creds)

if not res.success:
    print(f"operation:  {res.operation}")   # "login"
    print(f"context:    {res.context}")     # MT5 API function name
    print(f"error code: {res.error_code}")  # e.g. 10013
    print(f"message:    {res.error_message}")
```

```text
operation:  login
context:    login
error code: 10013
message:    Invalid account
```

---

## SDK-internal errors

Some errors originate inside the SDK, not from MT5. These use negative error codes:

| Code | Meaning |
|---|---|
| `-10` | `initialize()` was not called before this operation |

```python
mt5 = MetaTrader5Client()
res = mt5.positions()

# res.success == False
# res.error_code == -10
# res.error_message == "Client not initialized. Call initialize() first."
```

---

## Handling specific errors

```python
from syntiq_mt5 import constants

res = mt5.order_send(request)

if not res.success:
    # SDK-level failure (connection, not initialized, etc.)
    print(f"SDK error {res.error_code}: {res.error_message}")
elif not res.data.is_successful:
    # Broker rejected the order
    retcode = res.data.retcode
    if retcode == constants.TRADE_RETCODE_NO_MONEY:
        print("Insufficient funds")
    elif retcode == constants.TRADE_RETCODE_MARKET_CLOSED:
        print("Market is closed")
    elif retcode == constants.TRADE_RETCODE_REQUOTE:
        print(f"Requote — new price: {res.data.ask}")
    else:
        print(f"Order rejected: {res.data.comment} (retcode {retcode})")
else:
    print(f"Order filled: deal={res.data.deal}, order={res.data.order}")
```

---

## Two-level check for trade operations

`order_send()` and `order_check()` have two layers of success:

1. **`res.success`** — did the SDK call succeed (connection, parsing, etc.)?
2. **`res.data.is_successful`** — did the broker accept the trade?

```python
res = mt5.order_send(request)

if res.success and res.data.is_successful:
    print("Trade accepted")
elif res.success and not res.data.is_successful:
    print(f"Trade rejected by broker: {res.data.comment}")
else:
    print(f"SDK error: {res.error_message}")
```

---

## Exception classes

Exceptions are reserved for unrecoverable situations that cannot return a `Result` (e.g. during object construction). You will not encounter these in normal usage.

| Exception | When raised |
|---|---|
| `MT5Error` | Base class for all SDK exceptions |
| `MT5ConnectionError` | Unrecoverable connection lifecycle failure |
| `MT5ExecutionError` | Unrecoverable data retrieval or trade execution failure |
