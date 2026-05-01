# Get Account Info

Retrieve balance, equity, margin, and account settings.

---

## Basic account info

```python
res = mt5.account_info()

if res.success:
    acc = res.data
    print(f"Account:      #{acc.login}  {acc.name}")
    print(f"Broker:       {acc.company}  ({acc.server})")
    print(f"Balance:      {acc.balance:.2f} {acc.currency}")
    print(f"Equity:       {acc.equity:.2f} {acc.currency}")
    print(f"Margin:       {acc.margin:.2f} {acc.currency}")
    print(f"Free margin:  {acc.margin_free:.2f} {acc.currency}")
    print(f"Margin level: {acc.margin_level:.1f}%")
    print(f"Leverage:     1:{acc.leverage}")
else:
    print(f"Error {res.error_code}: {res.error_message}")
```

```text
Account:      #12345678  John Smith
Broker:       IC Markets  (ICMarkets-Demo)
Balance:      10000.00 USD
Equity:       10150.00 USD
Margin:       100.00 USD
Free margin:  10050.00 USD
Margin level: 10150.0%
Leverage:     1:100
```

---

## Computed properties

```python
acc = res.data

print(f"Margin used:          {acc.margin_used_percent:.1f}%")
print(f"Equity/balance ratio: {acc.equity_to_balance_ratio:.4f}")
```

| Property | Formula | Meaning |
|---|---|---|
| `margin_used_percent` | `margin / equity * 100` | How much of equity is tied up in margin |
| `equity_to_balance_ratio` | `equity / balance` | >1.0 = positions in profit; <1.0 = in loss |

---

## Terminal info

```python
res = mt5.terminal_info()

if res.success:
    term = res.data
    print(f"Build:         {term.build}")
    print(f"Connected:     {term.connected}")
    print(f"Trade allowed: {term.trade_allowed}")
    print(f"Ready:         {term.is_ready_for_trading}")
    print(f"Ping:          {term.ping_last} ms")
```

```text
Build:         4000
Connected:     True
Trade allowed: True
Ready:         True
Ping:          42 ms
```

`is_ready_for_trading` is `True` only when `connected`, `trade_allowed`, and `not tradeapi_disabled` are all satisfied.

---

## Key AccountInfo fields

| Field | Description |
|---|---|
| `login` | Account number |
| `name` | Account holder name |
| `server` | Broker server name |
| `currency` | Account currency (e.g. `"USD"`) |
| `leverage` | Account leverage (e.g. `100` for 1:100) |
| `balance` | Account balance |
| `equity` | Balance + floating P&L |
| `margin` | Margin currently in use |
| `margin_free` | Available margin for new positions |
| `margin_level` | Equity / margin × 100 |
| `profit` | Total floating P&L across all open positions |
| `trade_allowed` | Whether trading is enabled |
