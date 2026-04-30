# MetaTrader5 Wrapper

> **The MetaTrader5 API should have been like this.**

Typed, predictable, and production-oriented access to the official `MetaTrader5` Python package.

## Why this exists
The official MT5 module is powerful but difficult to operate safely at scale:

- `last_error()` is global mutable state.
- Return types are inconsistent (`None`, `False`, tuples, numpy records).
- API usage encourages procedural flows that are easy to misuse.

`metatrader5_wrapper` fixes this with:

- a stateful `MetaTrader5Client`
- typed `Result[T]` responses
- per-operation error capture and context
- typed domain models (`Position`, `Candle`)

## Quickstart
```python
from pydantic import SecretStr
from metatrader5_wrapper import LoginCredentials, MetaTrader5Client

creds = LoginCredentials(login=123456, password=SecretStr("secret"), server="Broker-Demo")

with MetaTrader5Client() as client:
    client.initialize(creds)
    client.login(creds)
    positions = client.positions()
```

## Result[T] usage
```python
result = client.positions()

if result.success:
    for p in result.data:
        print(p.symbol, p.pips_profit)
else:
    print(result.error_code, result.error_message, result.context)
```

## Reliability guarantees
- `mt5.last_error()` is captured once per MT5 operation and bound to that operation.
- Client lifecycle is guarded (`initialize` before `login`/data calls).
- Empty datasets are treated as valid successes (`[]`).
- Malformed payloads return structured failures, not random crashes.
