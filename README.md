# MetaTrader5 Wrapper

> **The API MetaTrader5 should have shipped.**

## Why this exists
The official `MetaTrader5` Python module is powerful but procedural, globally stateful, and weakly typed. This package provides a structured, typed, and predictable SDK-like interface.

## Problems with official MT5
- Global `last_error()` state that is easy to lose.
- Function returns are often ambiguous (`None` vs `False` vs payload).
- Low discoverability for app teams and API consumers.

## Before / After

### Before
```python
import MetaTrader5 as mt5
mt5.initialize()
positions = mt5.positions_get()
print(mt5.last_error())
```

### After
```python
from metatrader5_wrapper import LoginCredentials, MetaTrader5Client
from pydantic import SecretStr

creds = LoginCredentials(login=123456, password=SecretStr("secret"), server="Broker-Demo")

with MetaTrader5Client() as client:
    client.initialize(creds)
    client.login(creds)
    result = client.positions()
    if result.success:
        print(result.data)
```

## Quickstart
1. Initialize terminal
2. Login
3. Fetch positions / candles
4. Shutdown handled by context manager

## Features
- Strongly typed result model: `Result[T]`
- Per-operation `last_error()` capture (never lost)
- Typed `Position` and `Candle` models
- Smart pip calculations from `symbol_info.point` and `symbol_info.digits`
- Idempotent connection lifecycle (`initialize` / `login` / `shutdown`)
