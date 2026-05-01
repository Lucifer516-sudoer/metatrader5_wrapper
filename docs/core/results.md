# Result[T]

Every client method returns `Result[T]`. No exceptions are raised for operational failures.

---

## Structure

```python
class Result(Generic[T]):
    success: bool           # True = operation succeeded
    data: T | None          # set on success, always None on failure
    error_code: int | None  # MT5 error code on failure
    error_message: str | None  # human-readable description on failure
    context: str | None     # MT5 API function name (e.g. "positions_get")
    operation: str | None   # logical operation name
```

The model enforces a strict invariant:

- `success=True` → `data` is set, error fields are `None`
- `success=False` → `data` is `None`, `error_code` and `error_message` are set

---

## Basic usage

```python
from syntiq_mt5 import constants

res = mt5.get_candles("EURUSD", timeframe=constants.TIMEFRAME_H1, count=10)

if res.success:
    for candle in res.data:
        print(f"O={candle.open}  H={candle.high}  L={candle.low}  C={candle.close}")
else:
    print(f"[{res.context}] error {res.error_code}: {res.error_message}")
```

---

## Success path

```python
res = mt5.positions()

if res.success:
    print(f"{len(res.data)} open positions")
    for p in res.data:
        print(f"  {p.symbol}  {p.pips_profit:+.1f} pips")
```

`res.data` is always the correct type — `list[Position]` here. No casting needed.

---

## Failure path

```python
res = mt5.positions()

if not res.success:
    print(f"operation:  {res.operation}")
    print(f"error code: {res.error_code}")
    print(f"message:    {res.error_message}")
```

```text
operation:  positions_get
error code: -10
message:    Client not initialized. Call initialize() first.
```

---

## Empty vs failure

A successful call with no data is **not** a failure:

```python
res = mt5.positions()

if res.success:
    if not res.data:
        print("No open positions")   # success, but empty list
    else:
        print(f"{len(res.data)} positions")
```

`res.success` tells you whether the call worked. `res.data` tells you what came back.

---

## Chaining calls

```python
def get_position_symbols(mt5: MetaTrader5Client) -> list[str]:
    res = mt5.positions()
    if not res.success:
        return []
    return [p.symbol for p in res.data]
```

Keep the pattern consistent: check `success`, then use `data`.
