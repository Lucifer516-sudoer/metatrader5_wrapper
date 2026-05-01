# Handle Errors

Patterns for handling failures at every level.

---

## Basic pattern

```python
res = mt5.positions()

if res.success:
    # use res.data
    print(f"{len(res.data)} positions")
else:
    print(f"[{res.operation}] error {res.error_code}: {res.error_message}")
```

---

## Lifecycle errors

Always check `initialize()` and `login()` before proceeding:

```python
init = mt5.initialize(creds)
if not init.success:
    raise SystemExit(f"initialize failed: {init.error_message}")

login = mt5.login(creds)
if not login.success:
    raise SystemExit(f"login failed ({login.error_code}): {login.error_message}")
```

Common login errors:

| Error code | Cause |
|---|---|
| `10013` | Invalid account number or password |
| `10014` | Wrong server name |
| `-10` | `initialize()` was not called first |

---

## Trade errors (two-level check)

`order_send()` can fail at the SDK level or be rejected by the broker:

```python
res = mt5.order_send(request)

if not res.success:
    # SDK-level failure
    print(f"SDK error {res.error_code}: {res.error_message}")

elif not res.data.is_successful:
    # Broker rejected the trade
    from syntiq_mt5 import constants
    retcode = res.data.retcode

    if retcode == constants.TRADE_RETCODE_NO_MONEY:
        print("Insufficient funds")
    elif retcode == constants.TRADE_RETCODE_MARKET_CLOSED:
        print("Market is closed")
    elif retcode == constants.TRADE_RETCODE_INVALID_STOPS:
        print("Invalid SL/TP levels")
    elif retcode == constants.TRADE_RETCODE_REQUOTE:
        print(f"Requote — new price: {res.data.ask}")
    else:
        print(f"Rejected (retcode {retcode}): {res.data.comment}")

else:
    print(f"Order filled: deal={res.data.deal}")
```

---

## Validate before sending

Use `order_check()` to catch problems before they reach the broker:

```python
check = mt5.order_check(request)

if check.success and check.data.is_successful:
    res = mt5.order_send(request)
    ...
else:
    reason = check.data.comment if check.success else check.error_message
    print(f"Pre-flight failed: {reason}")
```

---

## Logging errors

```python
import logging

log = logging.getLogger(__name__)

res = mt5.positions()
if not res.success:
    log.error(
        "positions failed",
        extra={
            "operation": res.operation,
            "error_code": res.error_code,
            "error_message": res.error_message,
        },
    )
```

---

## Result fields for debugging

| Field | When set | Description |
|---|---|---|
| `success` | always | `True` / `False` |
| `data` | on success | The return value |
| `error_code` | on failure | MT5 error code (negative = SDK-internal) |
| `error_message` | on failure | Human-readable description |
| `context` | on failure | MT5 API function name (e.g. `"positions_get"`) |
| `operation` | on failure | Logical operation name |

See [Result\[T\]](../core/results.md) and [Error Handling](../core/error-handling.md) for the full picture.
