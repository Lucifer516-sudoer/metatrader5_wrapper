# Getting Started

```python
from metatrader5_wrapper import LoginCredentials, MetaTrader5Client
from pydantic import SecretStr

creds = LoginCredentials(login=123456, password=SecretStr("secret"), server="Broker-Demo")

with MetaTrader5Client() as client:
    client.initialize(creds)
    client.login(creds)
    positions = client.positions()
    candles = client.get_candles("EURUSD", timeframe=1, count=100)
```
