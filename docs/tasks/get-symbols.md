# Get Symbols

List available symbols, query their specifications, and get the current tick.

---

## List all symbols

```python
res = mt5.symbols_get()

if res.success:
    print(f"Total: {len(res.data)}")
    print("First 5:", res.data[:5])
```

```text
Total: 120
First 5: ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD']
```

---

## Filter by group pattern

```python
res = mt5.symbols_get(group="*USD*")

if res.success:
    print(res.data)
```

```text
['EURUSD', 'GBPUSD', 'AUDUSD', 'USDCAD', 'USDCHF', ...]
```

---

## Symbol specification

```python
res = mt5.symbol_info("EURUSD")

if res.success:
    info = res.data
    print(f"Digits:        {info.digits}")
    print(f"Spread:        {info.spread_pips:.1f} pips")
    print(f"Contract size: {info.contract_size}")
    print(f"Min volume:    {info.volume_min}")
    print(f"Max volume:    {info.volume_max}")
    print(f"Volume step:   {info.volume_step}")
    print(f"Pip size:      {info.pip_size}")
```

```text
Digits:        5
Spread:        1.5 pips
Contract size: 100000.0
Min volume:    0.01
Max volume:    100.0
Volume step:   0.01
Pip size:      0.0001
```

---

## Current tick

```python
res = mt5.symbol_info_tick("EURUSD")

if res.success:
    tick = res.data
    print(f"Bid:    {tick.bid}")
    print(f"Ask:    {tick.ask}")
    print(f"Spread: {tick.spread:.5f}")
    print(f"Mid:    {tick.mid_price:.5f}")
```

```text
Bid:    1.08450
Ask:    1.08465
Spread: 0.00015
Mid:    1.08458
```

---

## Add/remove from Market Watch

```python
# Add BTCUSD to Market Watch
res = mt5.symbol_select("BTCUSD", enable=True)

# Remove it
res = mt5.symbol_select("BTCUSD", enable=False)
```

A symbol must be in Market Watch before you can trade it or fetch its data.

---

## Key SymbolInfo fields

| Field | Description |
|---|---|
| `name` | Symbol name |
| `digits` | Decimal places in price |
| `point` | Smallest price increment |
| `pip_size` | Pip size (accounts for 3/5-digit symbols) |
| `spread` | Current spread in points |
| `spread_pips` | Current spread in pips (computed) |
| `bid` / `ask` | Current bid/ask prices |
| `volume_min` | Minimum trade volume |
| `volume_max` | Maximum trade volume |
| `volume_step` | Volume increment |
| `trade_contract_size` | Contract size (e.g. 100000 for standard Forex lot) |
| `currency_base` | Base currency |
| `currency_profit` | Profit currency |
