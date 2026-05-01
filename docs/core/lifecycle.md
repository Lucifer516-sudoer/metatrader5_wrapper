# Lifecycle

Every session follows the same four steps.

```
initialize() → login() → use → shutdown()
```

---

## The pattern

```python
from pydantic import SecretStr
from syntiq_mt5 import LoginCredential, MetaTrader5Client

creds = LoginCredential(
    login=12345678,
    password=SecretStr("your-password"),
    server="Broker-Demo",
)

with MetaTrader5Client() as mt5:
    init = mt5.initialize(creds)
    if not init.success:
        raise SystemExit(f"initialize failed: {init.error_message}")

    login = mt5.login(creds)
    if not login.success:
        raise SystemExit(f"login failed: {login.error_message}")

    # all operations go here
    res = mt5.account_info()
    ...

# shutdown() is called automatically here
```

---

## Step by step

### `initialize(creds)`

Connects to the MT5 terminal process on your machine. The terminal must already be running.

- Accepts optional `path` in `LoginCredential` to locate `terminal64.exe`
- Must succeed before any other call
- Sets an internal `_initialized` flag — all other methods check this flag and fail fast if it is not set

### `login(creds)`

Authenticates with the broker server using your account number, password, and server name.

- Requires a successful `initialize()` first
- `server` must match exactly what appears in the MT5 terminal (e.g. `"ICMarkets-Demo"`)

### Use the client

All data and trading operations are available after a successful login. See the [Tasks](../tasks/get-positions.md) section for copy-paste examples.

### `shutdown()`

Disconnects from the terminal. Called automatically when the `with` block exits — even if an exception occurs.

---

## Common mistakes

**Calling methods before `initialize()`**

```python
mt5 = MetaTrader5Client()
res = mt5.positions()  # fails immediately
# res.success == False
# res.error_message == "Client not initialized. Call initialize() first."
```

**Not checking `initialize()` result**

```python
mt5.initialize(creds)   # silently fails if terminal is not running
mt5.login(creds)        # also fails — but with a confusing error
```

Always check `result.success` after `initialize()` and `login()`.

**Wrong server name**

The `server` field must match the broker server name exactly as shown in the MT5 terminal's login screen. A mismatch causes `login()` to fail with an authentication error.

---

## Debug mode

Enable per-call timing and status logging:

```python
with MetaTrader5Client(debug=True) as mt5:
    mt5.initialize(creds)
    mt5.login(creds)
    mt5.positions()
```

```text
[MT5] initialize | success | code=0 | 142ms
[MT5] login | success | code=0 | 87ms
[MT5] positions_get | success | code=0 | 12ms
```

Logs are emitted at `DEBUG` level via the `syntiq_mt5` logger.
