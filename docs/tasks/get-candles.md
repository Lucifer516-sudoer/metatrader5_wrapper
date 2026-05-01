# Get Candles

Fetch OHLCV bars using a count, a start date, or a date range.

---

## Most recent N bars

```python
from syntiq_mt5 import constants

res = mt5.get_candles("EURUSD", timeframe=constants.TIMEFRAME_H1, count=10)

if res.success:
    for c in res.data:
        print(f"O={c.open}  H={c.high}  L={c.low}  C={c.close}  vol={c.tick_volume}")
else:
    print(f"Error {res.error_code}: {res.error_message}")
```

```text
O=1.08320  H=1.08450  L=1.08290  C=1.08410  vol=1842
O=1.08410  H=1.08520  L=1.08380  C=1.08490  vol=2103
...
```

---

## From a specific date

```python
from datetime import datetime, timezone
from syntiq_mt5 import constants

date_from = datetime(2024, 6, 1, tzinfo=timezone.utc)

res = mt5.copy_rates_from("EURUSD", constants.TIMEFRAME_D1, date_from, count=30)

if res.success:
    print(f"Bars retrieved: {len(res.data)}")
```

---

## Date range

```python
from datetime import datetime, timezone
from syntiq_mt5 import constants

date_from = datetime(2024, 6, 1, tzinfo=timezone.utc)
date_to   = datetime(2024, 6, 30, tzinfo=timezone.utc)

res = mt5.copy_rates_range("EURUSD", constants.TIMEFRAME_H4, date_from, date_to)

if res.success:
    print(f"Bars in range: {len(res.data)}")
    last = res.data[-1]
    print(f"Last close: {last.close}")
```

---

## Timeframe constants

| Constant | Period |
|---|---|
| `TIMEFRAME_M1` | 1 minute |
| `TIMEFRAME_M5` | 5 minutes |
| `TIMEFRAME_M15` | 15 minutes |
| `TIMEFRAME_M30` | 30 minutes |
| `TIMEFRAME_H1` | 1 hour |
| `TIMEFRAME_H4` | 4 hours |
| `TIMEFRAME_D1` | 1 day |
| `TIMEFRAME_W1` | 1 week |
| `TIMEFRAME_MN1` | 1 month |

Full list in [Constants → Timeframes](../reference/constants.md#timeframes).

---

## Candle fields

| Field | Type | Description |
|---|---|---|
| `time` | `int` | Bar open time (Unix seconds) |
| `open` | `float` | Opening price |
| `high` | `float` | Highest price |
| `low` | `float` | Lowest price |
| `close` | `float` | Closing price |
| `tick_volume` | `int` | Number of price ticks |
| `spread` | `int` | Spread in points at bar open |
| `real_volume` | `int` | Traded volume (exchange only; 0 for Forex) |

---

## Method summary

| Method | Use when |
|---|---|
| `get_candles(symbol, timeframe, count)` | You want the N most recent bars |
| `copy_rates_from(symbol, timeframe, date_from, count)` | You want N bars starting from a date |
| `copy_rates_range(symbol, timeframe, date_from, date_to)` | You want all bars in a date range |
