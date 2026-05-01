# Get Positions

Fetch all open positions, optionally filtered by symbol.

---

## All positions

```python
res = mt5.positions()

if res.success:
    print(f"Open positions: {len(res.data)}")
    for p in res.data:
        print(f"  {p.symbol}  {'BUY' if p.is_buy else 'SELL'}  {p.volume} lots  {p.pips_profit:+.1f} pips")
else:
    print(f"Error {res.error_code}: {res.error_message}")
```

```text
Open positions: 2
  EURUSD  BUY  0.10 lots  +12.3 pips
  GBPUSD  SELL  0.05 lots  -4.7 pips
```

---

## Filter by symbol

```python
res = mt5.positions(symbol="EURUSD")

if res.success:
    for p in res.data:
        print(f"ticket={p.ticket}  open={p.price_open}  current={p.price_current}")
```

```text
ticket=123456  open=1.08450  current=1.08573
```

---

## Count only

```python
res = mt5.positions_total()

if res.success:
    print(f"Total open: {res.data}")
```

---

## Key fields

| Field | Type | Description |
|---|---|---|
| `ticket` | `int` | Unique position identifier |
| `symbol` | `str` | Trading instrument (e.g. `"EURUSD"`) |
| `type` | `PositionType` | `BUY` or `SELL` |
| `volume` | `float` | Position size in lots |
| `price_open` | `float` | Entry price |
| `price_current` | `float` | Current market price |
| `sl` | `float` | Stop loss price (`0.0` if not set) |
| `tp` | `float` | Take profit price (`0.0` if not set) |
| `profit` | `float` | Floating P&L in account currency |
| `swap` | `float` | Accumulated swap charges |
| `pips_profit` | `float` | Floating P&L in pips (computed) |
| `pips_to_tp` | `float` | Distance to take profit in pips (computed) |

---

## Computed properties

`pips_profit` and `pips_to_tp` account for 3/5-digit symbols automatically — no manual pip size calculation needed.

```python
p = res.data[0]

print(f"P&L:       {p.profit:.2f} {acc.currency}")
print(f"Pips:      {p.pips_profit:+.1f}")
print(f"To TP:     {p.pips_to_tp:.1f} pips")
print(f"Direction: {'long' if p.is_buy else 'short'}")
```
