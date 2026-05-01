# Get Ticks

Retrieve raw tick data for analysis and backtesting.

---

## Ticks from a start date

```python
from datetime import datetime, timezone
from syntiq_mt5 import constants

date_from = datetime(2024, 6, 1, 9, 0, tzinfo=timezone.utc)

res = mt5.copy_ticks_from(
    "EURUSD",
    date_from,
    count=500,
    flags=constants.COPY_TICKS_ALL,
)

if res.success:
    print(f"Ticks: {len(res.data)}")
    t = res.data[0]
    print(f"  time={t.time}  bid={t.bid}  ask={t.ask}  spread={t.spread:.5f}")
else:
    print(f"Error {res.error_code}: {res.error_message}")
```

```text
Ticks: 500
  time=1717232400  bid=1.08450  ask=1.08465  spread=0.00015
```

---

## Ticks in a date range

```python
from datetime import datetime, timezone
from syntiq_mt5 import constants

date_from = datetime(2024, 6, 1, tzinfo=timezone.utc)
date_to   = datetime(2024, 6, 1, 1, 0, tzinfo=timezone.utc)  # 1 hour

res = mt5.copy_ticks_range(
    "EURUSD",
    date_from,
    date_to,
    flags=constants.COPY_TICKS_ALL,
)

if res.success:
    print(f"Ticks in range: {len(res.data)}")
```

---

## Tick flags

Choose which ticks to retrieve:

| Constant | Description |
|---|---|
| `COPY_TICKS_ALL` | All ticks (bid/ask changes + trade ticks) |
| `COPY_TICKS_INFO` | Only bid/ask price changes |
| `COPY_TICKS_TRADE` | Only last price and volume changes (exchange instruments) |

For Forex, use `COPY_TICKS_INFO` or `COPY_TICKS_ALL`. `COPY_TICKS_TRADE` is for exchange instruments with real volume.

---

## Tick fields

| Field | Description |
|---|---|
| `time` | Tick time (Unix seconds) |
| `time_msc` | Tick time (milliseconds) |
| `bid` | Bid price |
| `ask` | Ask price |
| `last` | Last trade price (exchange only; 0.0 for Forex) |
| `volume` | Last trade volume (exchange only) |
| `flags` | Bitmask of `TICK_FLAG_*` constants |
| `spread` | `ask - bid` (computed) |
| `mid_price` | `(bid + ask) / 2` (computed) |
| `has_bid` | `True` if bid changed in this tick |
| `has_ask` | `True` if ask changed in this tick |

---

## Inspect what changed in a tick

```python
from syntiq_mt5 import constants

for tick in res.data[:10]:
    changed = []
    if tick.has_bid:
        changed.append(f"bid={tick.bid}")
    if tick.has_ask:
        changed.append(f"ask={tick.ask}")
    print(f"  t={tick.time_msc}ms  {', '.join(changed)}")
```
