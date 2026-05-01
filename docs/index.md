# syntiq-mt5

A typed, minimal Python SDK for the MetaTrader 5 API.

Every call returns `Result[T]` — no exceptions, no magic numbers, no guessing.

---

## Why syntiq-mt5?

The raw `MetaTrader5` Python package returns untyped structs, stores errors in global state, and requires you to know integer constants by heart. `syntiq-mt5` fixes all of that:

| Raw MT5 | syntiq-mt5 |
|---|---|
| Untyped namedtuples | Pydantic models with IDE completion |
| `mt5.last_error()` after every call | `result.error_code` / `result.error_message` |
| Magic integers (`0`, `1`, `16385`) | Named constants (`ORDER_TYPE_BUY`, `TIMEFRAME_H1`) |
| Raises on connection failure | Returns `Result.fail(...)` |
| Manual `mt5.shutdown()` | Automatic via context manager |

---

## Install

```bash
pip install syntiq-mt5
```

**Requirements:** MetaTrader 5 terminal installed · Windows · Python 3.12+

---

## 60-second example

```python
from pydantic import SecretStr
from syntiq_mt5 import LoginCredential, MetaTrader5Client, constants

creds = LoginCredential(
    login=12345678,
    password=SecretStr("your-password"),
    server="Broker-Demo",
)

with MetaTrader5Client() as mt5:
    mt5.initialize(creds)
    mt5.login(creds)

    res = mt5.positions()
    if res.success:
        for p in res.data:
            print(f"{p.symbol}  {p.volume} lots  {p.pips_profit:+.1f} pips")
```

```text
EURUSD  0.10 lots  +12.3 pips
GBPUSD  0.05 lots  -4.7 pips
```

---

## Where to go next

- **[Quickstart](getting-started.md)** — full working example in under 60 seconds
- **[Lifecycle](core/lifecycle.md)** — understand `initialize → login → use → shutdown`
- **[Result\[T\]](core/results.md)** — how every call returns success or failure
- **[Tasks](tasks/get-positions.md)** — copy-paste recipes for every operation
