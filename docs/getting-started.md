# Quickstart

Get from install to live data in under 60 seconds.

---

## Prerequisites

- **Windows** — the MT5 Python API is Windows-only
- **MetaTrader 5 terminal** installed ([download](https://www.metatrader5.com/en/download))
- A valid MT5 account (demo accounts work fine)
- Python 3.12+

---

## Install

```bash
pip install syntiq-mt5
```

---

## Minimal working example

```python
from pydantic import SecretStr
from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(
    login=12345678,                        # your MT5 account number
    password=SecretStr("your-password"),   # stored as a secret — never logged
    server="Broker-Demo",                  # broker server name from MT5 terminal
)

with MetaTrader5Client() as mt5:
    # 1. Connect to the terminal
    init = mt5.initialize(creds)
    if not init.success:
        print(f"Initialize failed: {init.error_message}")
        raise SystemExit(1)

    # 2. Authenticate with the broker
    login = mt5.login(creds)
    if not login.success:
        print(f"Login failed: {login.error_message}")
        raise SystemExit(1)

    # 3. Fetch open positions
    res = mt5.positions()
    if res.success:
        print(f"Open positions: {len(res.data)}")
        for p in res.data:
            print(f"  {p.symbol}  {p.volume} lots  {p.pips_profit:+.1f} pips")
    else:
        print(f"Error {res.error_code}: {res.error_message}")

# mt5.shutdown() is called automatically when the `with` block exits
```

**Example output:**

```text
Open positions: 2
  EURUSD  0.10 lots  +12.3 pips
  GBPUSD  0.05 lots  -4.7 pips
```

---

## What just happened?

| Step | Method | What it does |
|---|---|---|
| 1 | `initialize(creds)` | Connects to the MT5 terminal process |
| 2 | `login(creds)` | Authenticates with the broker server |
| 3 | `positions()` | Returns all open positions |
| — | `with` block exit | Calls `shutdown()` automatically |

Every method returns `Result[T]`. Check `result.success` before accessing `result.data`.

---

## Next steps

- **[Lifecycle](core/lifecycle.md)** — common mistakes and the full connection flow
- **[Result\[T\]](core/results.md)** — how to handle success and failure
- **[Get Candles](tasks/get-candles.md)** — fetch OHLCV price data
- **[Place Orders](tasks/place-orders.md)** — validate and send trade requests
