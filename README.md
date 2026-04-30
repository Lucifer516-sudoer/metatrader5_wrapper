# MetaTrader5 Wrapper

> **The API MetaTrader5 should have shipped.**

A minimal, typed, production-oriented wrapper for the official `MetaTrader5` Python package.

## Installation

```bash
pip install metatrader5-wrapper
```

For development:

```bash
pip install -e .[dev]
```

## Quickstart

```python
from pydantic import SecretStr
from metatrader5_wrapper import LoginCredential, MetaTrader5Client

creds = LoginCredential(login=12345678, password=SecretStr("your-password"), server="Broker-Demo")

with MetaTrader5Client() as client:
    client.initialize(creds)
    client.login(creds)
    positions = client.positions()
```

## Why this exists

The official MT5 API is powerful but awkward for production Python:

- global mutable `last_error()` state
- inconsistent return types
- procedural flow that's easy to misuse

This wrapper provides:

- typed `Result[T]` responses
- operation-bound error capture
- explicit client lifecycle guards
- typed `Position` and `Candle` models

## Result[T] example

```python
result = client.get_candles("EURUSD", timeframe=1, count=50)

if result.success:
    print("Loaded", len(result.data or []), "candles")
else:
    print(
        "Operation failed:",
        result.operation,
        result.error_code,
        result.error_message,
    )
```

Example failure output:

```text
Operation failed: login 10013 Invalid account
```

## Public API

- `MetaTrader5Client`
- `LoginCredential`
- `Result`
- `Position`
- `Candle`

## Versioning

This project follows **Semantic Versioning**.

- `0.1.x`: early public releases, rapid improvements
- `0.y.z`: potentially breaking changes before `1.0`
- `1.0+`: stable public API guarantees
